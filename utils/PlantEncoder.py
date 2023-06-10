import zlib
import base64
import string

plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
base64_alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'


def encode(diagram: str, render_type: str) -> str:
    """
    Encodes a PlantUML diagram, so it can be passed to the online renderer.

    :param diagram: The diagram to encode.
    :param render_type: A valid render type string (`uml`, `png`, `svg`, `txt`).
    :return: The encoded URI component.
    """
    return 'http://www.plantuml.com/plantuml/' + render_type + '/' + base64.b64encode(
        zlib.compress(diagram.encode('utf-8'))[2:-4]).translate(
        bytes.maketrans(base64_alphabet.encode('utf-8'), plantuml_alphabet.encode('utf-8'))).decode(
        'utf-8')
