"""C01 supervisor for one empty/prepared company on its OWN persistent disk."""
from __future__ import annotations
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from .provision import DemoError
from .company_provision import prepare_company
from .company_nginx import render_company

BASE=Path('/opt/wavelink')
MOUNT=Path('/var/data')
DATA=MOUNT/'wavelink-company'
APP_PORT=8765


def run_company():
    from .entrypoint import mounted, minimal_environment, wait_ready
    os.umask(0o077)
    if not mounted(MOUNT):
        raise DemoError('Company mode requires its own persistent disk at /var/data. Refusing ephemeral storage.')
    if (MOUNT/'wavelink').exists() or (MOUNT/'DEPLOYMENT.json').exists():
        raise DemoError('This disk contains demonstration or other deployment storage. Use a NEW company disk; no changes made.')
    if DATA.is_symlink(): raise DemoError('Unsafe company storage root.')
    DATA.mkdir(mode=0o700, exist_ok=True)
    if os.geteuid()==0:
        os.chown(DATA,10001,10001)
        os.setgroups([]);os.setgid(10001);os.setuid(10001)
    port=int(os.environ.get('PORT','10000'))
    if not 1024<=port<=65535 or port==APP_PORT: raise DemoError('Invalid company public port.')
    cfg=prepare_company(DATA,BASE/'app',dict(os.environ),app_port=APP_PORT)
    runtime=Path('/tmp/wavelink-company-gateway');runtime.mkdir(mode=0o700,exist_ok=True)
    config=runtime/'nginx.conf';config.write_text(render_company(cfg['authority'],port,runtime))
    check=subprocess.run(['nginx','-t','-c',str(config)],env=minimal_environment(),stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    if check.returncode:
        raise DemoError('Company gateway configuration did not validate. Check restricted operator logs.')
    stop=False
    def request_stop(_sig,_frame):
        nonlocal stop
        stop=True
    signal.signal(signal.SIGTERM,request_stop);signal.signal(signal.SIGINT,request_stop)
    processes=[];exitcode=0
    try:
        env=minimal_environment();env['PYTHONPATH']=str(BASE/'app')
        core=subprocess.Popen([sys.executable,'-m','deploy.company_runtime','--config',str(cfg['config']),'--root',str(DATA)],cwd=BASE,env=env)
        processes.append(core);wait_ready(core,APP_PORT,'/readyz')
        nginx=subprocess.Popen(['nginx','-c',str(config),'-g','daemon off;'],env=minimal_environment())
        processes.append(nginx)
        print('Wavelink C01 company service started: one isolated project; named-account login; no demonstration guest. Platform/security/restore acceptance remains required.',flush=True)
        while not stop:
            if any(p.poll() is not None for p in processes):
                print('A company component stopped. Stopping all components; the project is retained.',flush=True);exitcode=1;break
            time.sleep(.5)
    finally:
        for p in reversed(processes):
            if p.poll() is None:p.terminate()
        deadline=time.monotonic()+35
        for p in reversed(processes):
            try:p.wait(timeout=max(.1,deadline-time.monotonic()))
            except subprocess.TimeoutExpired:p.kill();p.wait(timeout=5)
    return exitcode
