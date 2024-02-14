import zlib
import base64
import string

PLANTUML_ALPHABET: str = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
BASE64_ALPHABET: str = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'


def encode(diagram: str, render_type: str) -> str:
    """
    Encodes a PlantUML diagram, so it can be passed to the online renderer.

    :param diagram: The diagram to encode.
    :param render_type: A valid render type string (`uml`, `png`, `svg`, `txt`).
    :return: The encoded URI component.
    """
    return 'http://www.plantuml.com/plantuml/' + render_type + '/' + base64.b64encode(
        zlib.compress(diagram.encode('utf-8'))[2:-4]).translate(
        bytes.maketrans(BASE64_ALPHABET.encode('utf-8'), PLANTUML_ALPHABET.encode('utf-8'))).decode(
        'utf-8')
