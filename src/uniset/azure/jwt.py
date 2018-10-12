import base64
import json
import logging
import re

log = logging.getLogger(__name__)


def _azure_parse_jwt(id_token):
    jwt_token_parts = r"^([^\.\s]*)\.([^\.\s]+)\.([^\.\s]*)$"
    matches = re.search(jwt_token_parts, id_token)
    if not matches or len(matches.groups()) < 3:
        log.error('Unable to parse token.')
        return {}

    return {
        'header': matches.group(1),
        'Payload': matches.group(2),
        'Sig': matches.group(3)
    }


def _azure_jwt_token_parse(id_token):
    jwt_split_token = _azure_parse_jwt(id_token)
    if not jwt_split_token:
        return

    jwt_payload = jwt_split_token['Payload']
    # Prepare for base64 decoding
    payload_b64_string = jwt_payload
    payload_b64_string += '=' * (4 - ((len(jwt_payload) % 4)))
    decoded_payload = base64.urlsafe_b64decode(payload_b64_string.encode('ascii'))

    if not decoded_payload:
        log.error('Payload of id_token could not be base64 url decoded.')
        return
    jwt_decoded_payload = json.loads(decoded_payload.decode('utf-8'))

    return jwt_decoded_payload
