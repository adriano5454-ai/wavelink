"""Install synthetic avatar cases only in a disposable local browser-test store."""
import hashlib
import struct
import zlib


def install(store):
    def chunk(kind, data):
        return struct.pack('!I', len(data))+kind+data+struct.pack('!I', zlib.crc32(kind+data))
    png = (b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR', struct.pack('!2I5B',1,1,8,2,0,0,0))+
           chunk(b'IDAT',zlib.compress(bytes([0,52,130,145])))+chunk(b'IEND',b''))
    with store.connection(True) as c:
        for name, data in [('Davi Coral', png), ('Mara Brisa', b'invalid image')]:
            uid=c.execute('SELECT id FROM users WHERE name=?',(name,)).fetchone()[0]
            c.execute("INSERT OR IGNORE INTO member_profiles(user_id,version,created_at,updated_at,updated_by) VALUES(?,1,'test','test',?)",(uid,uid))
            c.execute("UPDATE member_profiles SET avatar_data=?,avatar_sha256=?,avatar_mime='image/png' WHERE user_id=?",
                      (data,hashlib.sha256(data).hexdigest(),uid))
