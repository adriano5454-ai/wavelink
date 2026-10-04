"""C01 supervisor for one empty/prepared company on its OWN persistent disk."""
from __future__ import annotations
import os
from collections.abc import Mapping
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

# M01: only the company application needs membership settings. Never forward
# arbitrary operator environment variables, bootstrap secrets, or demo passwords.
_MEMBERSHIP_SMTP_ENV = (
    'MEMBERSHIP_SMTP_HOST', 'MEMBERSHIP_SMTP_PORT', 'MEMBERSHIP_SMTP_TLS',
    'MEMBERSHIP_SMTP_USERNAME', 'MEMBERSHIP_SMTP_PASSWORD', 'MEMBERSHIP_SMTP_FROM',
)


def company_application_environment(source: Mapping[str, str], *, origin: str) -> dict[str, str]:
    """Build the private child environment after prepare_company validates identity.

    Keep the generic minimal_environment unchanged: Nginx and demo children must
    not receive company mail credentials. Use the validated canonical public
    origin, copy the password exactly, and let MembershipSettings retain its
    existing OFF/invalid-configuration fail-closed behaviour.
    """
    from .entrypoint import minimal_environment
    if source.get('WAVELINK_DEPLOYMENT_MODE', 'DEMO') != 'COMPANY':
        raise DemoError('Company application environment requires COMPANY mode.')
    env = minimal_environment()
    env.update(PYTHONPATH=str(BASE/'app'), WAVELINK_DEPLOYMENT_MODE='COMPANY',
               COMPANY_ID=source['COMPANY_ID'], COMPANY_NAME=source['COMPANY_NAME'],
               PUBLIC_URL=origin)
    mode = source.get('WAVELINK_MEMBERSHIP_MODE', 'OFF')
    env['WAVELINK_MEMBERSHIP_MODE'] = mode
    env['WAVELINK_ALERT_EMAIL'] = source.get('WAVELINK_ALERT_EMAIL', 'OFF')
    if mode == 'INVITE_ONLY':
        for name in _MEMBERSHIP_SMTP_ENV:
            if name in source:
                env[name] = source[name]
    return env


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
    operator_env=dict(os.environ)
    cfg=prepare_company(DATA,BASE/'app',operator_env,app_port=APP_PORT)
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
        env=company_application_environment(operator_env,origin=cfg['origin'])
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
