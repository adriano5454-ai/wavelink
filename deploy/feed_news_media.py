"""Package the native storage and image processing for optional news photos."""


def transforms():
    return {}


def additions():
    return {'app/feed_news_media.py': SOURCE}


SOURCE = '''"""Single, private display photo committed in the same transaction as its post."""
import base64
import io
import warnings

from PIL import Image, ImageOps

from .illustrations import MAX_INPUT_PIXELS
from .store import Problem


MAX_UPLOAD_BYTES = 5 * 1024 * 1024
FORMATS = {'data:image/jpeg;base64': 'JPEG', 'data:image/png;base64': 'PNG',
           'data:image/webp;base64': 'WEBP'}
MAX_DATA_URL_LENGTH = max(map(len, FORMATS)) + 1 + 4 * ((MAX_UPLOAD_BYTES + 2) // 3)


def prepare_image(image):
    if image is None:
        return None
    if not isinstance(image, str) or len(image) > MAX_DATA_URL_LENGTH:
        raise Problem(422, 'Choose a news image of 5 MiB or less.')
    header, separator, encoded = image.partition(',')
    expected = FORMATS.get(header)
    if not separator or not encoded or not expected:
        raise Problem(422, 'Choose a JPEG, PNG or WebP news image.')
    try:
        raw = base64.b64decode(encoded, validate=True)
    except ValueError:
        raise Problem(422, 'The news image could not be read. Choose the picture again.') from None
    if len(raw) > MAX_UPLOAD_BYTES:
        raise Problem(422, 'Choose a news image of 5 MiB or less.')

    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(raw), formats=[expected]) as check:
                if check.width * check.height > MAX_INPUT_PIXELS or getattr(check, 'n_frames', 1) != 1:
                    raise ValueError('dimensions or animation')
                check.verify()
            with Image.open(io.BytesIO(raw), formats=[expected]) as source:
                source.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
                photo = ImageOps.exif_transpose(source)
                # A fresh pixel canvas discards location, camera, and other metadata.
                canvas = Image.new('RGB', photo.size, 'white')
                if 'A' in photo.getbands() or 'transparency' in photo.info:
                    pixels = photo.convert('RGBA')
                    canvas.paste(pixels, mask=pixels.getchannel('A'))
                else:
                    canvas.paste(photo.convert('RGB'))
                out = io.BytesIO()
                canvas.save(out, 'JPEG', quality=83, optimize=True)
                return 'image/jpeg', out.getvalue()
    except (OSError, ValueError, SyntaxError, Image.DecompressionBombError,
            Image.DecompressionBombWarning):
        raise Problem(422, 'Choose a readable, still JPEG, PNG or WebP of up to 24 megapixels.') from None


def ensure(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS feed_news_images (
        post_id TEXT PRIMARY KEY REFERENCES feed_news_posts(id) ON DELETE CASCADE,
        content_type TEXT NOT NULL, content BLOB NOT NULL)""")


def store_image(conn, post_id, prepared):
    content_type, content = prepared
    conn.execute('INSERT INTO feed_news_images(post_id,content_type,content) VALUES (?,?,?)',
                 (post_id, content_type, content))


def load_image(conn, post_id):
    """Call only after checking the current actor can read the parent post."""
    row = conn.execute('SELECT content_type,content FROM feed_news_images WHERE post_id=?',
                       (post_id,)).fetchone()
    return (row[0], row[1]) if row is not None else None
'''
