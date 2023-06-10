import zlib
import base64
import string

plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
base64_alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'


def encode(text: str, render_type: str) -> str:
    return 'http://www.plantuml.com/plantuml/' + render_type + '/' + base64.b64encode(
        zlib.compress(text.encode('utf-8'))[2:-4]).translate(
        bytes.maketrans(base64_alphabet.encode('utf-8'), plantuml_alphabet.encode('utf-8'))).decode(
        'utf-8')
