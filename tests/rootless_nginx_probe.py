"""Local UID-10001 gateway check; never contacts Render or a project database."""
from pathlib import Path
import http.client
import json
import os
import socket
import subprocess
import sys
import tempfile
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from deploy.nginx_config import render


def run():
    if os.geteuid()!=0:
        raise RuntimeError('This optional UID-switching test needs an isolated root test container.')
    with tempfile.TemporaryDirectory(prefix='wavelink-rootless-gateway-') as tmp:
        root=Path(tmp);root.chmod(0o755)
        runtime=root/'nginx'
        with socket.socket() as s:
            s.bind(('127.0.0.1',0));port=s.getsockname()[1]
        text=render('demo.example.test',port,runtime,bind='127.0.0.1')
        config=runtime/'nginx.conf';config.write_text(text)
        for p in [runtime,*runtime.rglob('*')]:os.chown(p,10001,10001)
        env={'PATH':'/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin','HOME':'/tmp','LANG':'C.UTF-8'}
        result=subprocess.run(['nginx','-t','-c',str(config)],user=10001,group=10001,
                              extra_groups=[],env=env,text=True,capture_output=True)
        assert result.returncode==0,result.stderr
        p=subprocess.Popen(['nginx','-c',str(config),'-g','daemon off;'],user=10001,
                           group=10001,extra_groups=[],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:
            status=None
            for _ in range(30):
                assert p.poll() is None,'Rootless gateway exited'
                c=None
                try:
                    c=http.client.HTTPConnection('127.0.0.1',port,timeout=1)
                    c.request('GET','/',headers={'Host':'wrong.example.test'})
                    r=c.getresponse();status=r.status;r.read()
                    break
                except OSError:time.sleep(.1)
                finally:
                    if c:c.close()
            assert status==421,status
            assert (runtime/'error.log').exists()
            assert all((runtime/x).is_dir() for x in ['body','proxy','fastcgi','uwsgi','scgi'])
        finally:
            p.terminate()
            try:p.communicate(timeout=5)
            except subprocess.TimeoutExpired:p.kill();p.communicate(timeout=5)
    return {'passed':True,'effective_uid':10001,'nginx_version':subprocess.run(['nginx','-v'],text=True,capture_output=True).stderr.strip(),
            'checks':['Nginx configuration validation as UID 10001','Actual non-root listener, wrong-host rejection, runtime log and all five temporary directories'],
            'render_tested':False,'docker_built':False}

if __name__=='__main__':
    result=run()
    output=Path(os.environ.get('WAVELINK_ROOTLESS_OUTPUT','/tmp/wavelink-rootless-results.json'))
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
