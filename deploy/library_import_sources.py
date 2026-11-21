"""Keep the exact source of a confirmed workspace import in its own access scope."""
from collections import OrderedDict
from hashlib import sha256
from pathlib import PurePath
from threading import Lock
from time import monotonic

from .store import Problem, utcnow


MODULES = {'checklist': 'checklists', 'toolbox': 'toolbox', 'inventory': 'inventory',
           'maintenance': 'maintenance', 'logbook': 'logs'}
MIMES = {'.txt': 'text/plain', '.md': 'text/markdown', '.csv': 'text/csv',
         '.tsv': 'text/tab-separated-values', '.pdf': 'application/pdf', '.png': 'image/png',
         '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.tif': 'image/tiff',
         '.tiff': 'image/tiff', '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
         '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
         '.xlsm': 'application/vnd.ms-excel.sheet.macroEnabled.12'}


class PendingScans:
    """Short-lived compatibility for already-open clients that submit a reviewed hash."""
    def __init__(self):
        self.files = OrderedDict()
        self.lock = Lock()
        self.size = 0

    def remember(self, key, raw):
        now = monotonic()
        with self.lock:
            old = self.files.pop(key, None)
            if old:
                self.size -= len(old[1])
            while self.files and (self.size + len(raw) > 36_000_000 or
                                  next(iter(self.files.values()))[0] < now or len(self.files) >= 128):
                self.size -= len(self.files.popitem(last=False)[1][1])
            self.files[key] = (now + 1800, raw)
            self.size += len(raw)

    def read(self, key):
        with self.lock:
            entry = self.files.get(key)
            if entry and entry[0] >= monotonic():
                return entry[1]
        raise Problem(409, 'Reopen the original file and review it again to save this import.')


def ensure(c):
    c.execute('''CREATE TABLE IF NOT EXISTS workspace_file_imports (
        id TEXT PRIMARY KEY, kind TEXT NOT NULL, record_id TEXT NOT NULL, title TEXT NOT NULL,
        filename TEXT NOT NULL, mime TEXT NOT NULL, size INTEGER NOT NULL, sha256 TEXT NOT NULL,
        added_at TEXT NOT NULL, data BLOB NOT NULL)''')
    c.execute('CREATE INDEX IF NOT EXISTS workspace_file_kind ON workspace_file_imports(kind,record_id)')


def retain(c, op_id, kind, record, name, raw, digest):
    ensure(c)
    if not raw or kind not in MODULES or sha256(raw).hexdigest() != digest:
        raise Problem(409, 'The file no longer matches the reviewed source. Choose the original again.')
    mime = MIMES.get(PurePath(name).suffix.lower(), 'application/octet-stream')
    c.execute('INSERT INTO workspace_file_imports VALUES(?,?,?,?,?,?,?,?,?,?)',
              (op_id, kind, record['id'], record['title'], name, mime, len(raw), digest, utcnow(), raw))


def allowed(c, actor, token, kind):
    from .builder_hub import KINDS
    from .browser_admin import require_named_permission
    require_named_permission(c, actor, KINDS[kind][0], token, label='Import source')


def original_bytes(store, actor, token, file_id):
    from .original_folders import OriginalFolders
    with store.connection() as c:
        OriginalFolders._authorise(c, actor)
        row = c.execute('SELECT kind FROM workspace_file_imports WHERE id=?', (file_id,)).fetchone()
        if not row:
            raise Problem(404, 'Source file unavailable.')
        allowed(c, actor, token, row['kind'])
        row = c.execute('SELECT filename,mime,size,sha256,data FROM workspace_file_imports WHERE id=?', (file_id,)).fetchone()
        if len(row['data']) != row['size'] or sha256(row['data']).hexdigest() != row['sha256']:
            raise Problem(409, 'The stored file could not be verified.')
        return row['data'], row['mime'], row['filename']


def prune(c, chosen):
    for kind, module in MODULES.items():
        if module not in chosen or 'documents' not in chosen:
            c.execute('DELETE FROM workspace_file_imports WHERE kind=?', (kind,))
