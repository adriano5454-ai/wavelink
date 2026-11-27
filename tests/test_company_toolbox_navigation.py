"""Verify the narrow Toolbox backport against its company release artifacts."""
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess

import pytest


OVERLAY = runpy.run_path(str(
    Path(__file__).resolve().parents[1] / "deploy" / "apply_company_toolbox_navigation.py"
))
# The preview layout matches Demo. The two JS resources also handle an authenticated
# list refresh finishing while this workspace's read-only mobile sheet is open.
REVIEWED = {
    "app/static/fieldwork.js": "6e51068e10f2a5df1890bd68e2f57cb9b506fbed2f39b15d0ac8543f88c4017e",
    "app/static/toolbox_ui.js": "d5f020130e79b50bb14ddd2f366f8e9429c43a50c28af6a305292f4f0b1acbf9",
    "app/static/operations_workspace_ui76.css": "0c58a34095e4ef12598cb42b7c6f667fec4f534d4f94fa70df80476280a343c0",
}
METADATA = {"UI_PATCH.json", "app/static/index.html", "app/static/pt-BR/index.html", "app/static/sw.js"}


def test_rejects_unexpected_parent_without_writes(tmp_path):
    manifest = tmp_path / "RELEASE_FILES.json"
    manifest.write_bytes(b'{"files":{}}\n')
    with pytest.raises(ValueError, match="Unexpected company release before Toolbox"):
        OVERLAY["apply"](tmp_path)
    assert manifest.read_bytes() == b'{"files":{}}\n'
    assert list(tmp_path.iterdir()) == [manifest]


@pytest.fixture
def source():
    location = os.environ.get("WAVELINK_COMPANY_TOOLBOX_BASE")
    if not location:
        pytest.skip("Set WAVELINK_COMPANY_TOOLBOX_BASE to the extracted #69 program files")
    return Path(location)


def test_replay_preserves_company_release_and_second_run(tmp_path, source):
    manifest = "RELEASE_FILES.json"
    parent = (source / manifest).read_bytes()
    assert sha256(parent).hexdigest() == OVERLAY["PARENT"]
    files = json.loads(parent)["files"]
    # Copy only the shipped program file list, never a workspace or untracked data.
    for name in [*files, manifest]:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, target)

    OVERLAY["apply"](tmp_path)
    result = (tmp_path / manifest).read_bytes()
    assert sha256(result).hexdigest() == OVERLAY["RESULT"]
    after = json.loads(result)["files"]
    assert files.keys() == after.keys()
    assert {name for name in files if after[name] != files[name]} == REVIEWED.keys() | METADATA
    for name, expected in REVIEWED.items():
        assert after[name] == sha256((tmp_path / name).read_bytes()).hexdigest() == expected

    OVERLAY["apply"](tmp_path)
    assert (tmp_path / manifest).read_bytes() == result
    # An already-stamped manifest must not hide subsequent damage to an asset.
    (tmp_path / "app/static/fieldwork.js").write_bytes(b"changed fixture")
    with pytest.raises(ValueError, match="Unexpected resource: app/static/fieldwork.js"):
        OVERLAY["apply"](tmp_path)


def test_list_reads_and_editor_ownership(source):
    # Execute the shipped reader and guard with a controlled list response and
    # the minimal DOM surface they inspect; no server, identity or account data.
    transforms = OVERLAY["transforms"]()
    def script(name):
        name = "app/static/" + name
        return transforms[name]((source / name).read_text(encoding="utf-8"))

    field = script("fieldwork.js")
    start = field.index("async function openToolbox(")
    end = field.index("async function open({", start)
    programs = {"guard": script("toolbox_ui.js"), "read": field[start:end].strip()}
    test = r"""
const assert=require('node:assert/strict');
const {guard,read}=JSON.parse(require('node:fs').readFileSync(0,'utf8'));
async function check(kind){
 const state={hub_id:'company',auth:{person:{user_id:'viewer'},token:'session'}},location={hash:'#toolbox'};
 const original={id:'A',title:'Original'}, current={id:'A',title:'Updated'};
 const sheet={},other={},dlg={open:false},dialogs=[];
 const document={body:null,getElementById:()=>null,querySelector:()=>dialogs[0],querySelectorAll:()=>dialogs};
 const host={dataset:{fwRoute:'company:viewer|#toolbox'}},selected={dataset:{toolboxId:'A'}};
 const root={firstElementChild:host,querySelector:s=>({
  '.tb-workspace':host,'#tb-results [aria-current="true"]':selected,
  '.tb-preview-layout > dialog.tb-talk-preview[open]':dialogs.includes(sheet)?sheet:null
 }[s]||null)};
 const history={state:{routeIndex:2,tbPreview:{scope:'scope',id:'A'}},replaceState(s){this.state=s;}};
 const window={history},__wl118={t:s=>s},previewScope='scope',talkOrigin=null;
 eval('"use strict";'+guard);
 const AJToolboxUI=window.AJToolboxUI, owner=AJToolboxUI.capture();
 let toolboxViewKey=AJToolboxUI.key(),toolboxEpoch=0;
 let lastResponse=toolboxViewKey+location.hash+JSON.stringify({talks:[original]});
 const pageBusy=()=>false,permission=()=>true,message=e=>e.message;
 const painted=[],notices=[],toolboxHome=data=>painted.push(data.talks),toolboxReadNotice=()=>false;
 const toolboxNotice=(text,denied=false)=>{if(text)notices.push(denied?'denied':'interrupted');};
 async function api(path){
  assert.equal(path,'/api/toolbox');
  dialogs.push(sheet);
  if(kind==='editor')dlg.open=true;
  if(kind==='another-dialog')dialogs.push(other);
  if(kind==='denied'||kind==='editor')throw Object.assign(new Error('Access denied'),{status:403});
  return {talks:kind==='removed'?[]:[kind==='updated'?current:original]};
 }
 await eval('('+read+')')();
 assert.throws(()=>owner.before(),/Toolbox view changed/,'write authorization remains strict');
 assert.equal(history.state.routeIndex,2);
 if(kind==='same'){
  assert.deepEqual(notices,[]);assert.deepEqual(painted,[]);assert(history.state.tbPreview);
 }else if(kind==='updated'||kind==='removed'){
  assert.deepEqual(notices,[]);assert.deepEqual(painted,[kind==='updated'?[current]:[]]);
  assert.equal(Boolean(history.state.tbPreview),kind==='updated');
 }else if(kind==='denied'){
  assert.deepEqual(notices,['denied']);assert.deepEqual(painted,[]);assert(!history.state.tbPreview);
 }else{
  assert.deepEqual(notices,['interrupted']);assert.deepEqual(painted,[]);assert(history.state.tbPreview);
 }
}
(async()=>{for(const kind of ['same','updated','removed','denied','editor','another-dialog'])await check(kind);})()
 .catch(e=>{console.error(e);process.exitCode=1});
"""
    subprocess.run(["node", "-e", test], input=json.dumps(programs), text=True, check=True, timeout=20)
