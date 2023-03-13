import http.client
import json
import re
from typing import TypedDict


class Response(TypedDict):
    status: int
    json: dict


url_regex = r'(?:(?P<protocol>http[s]?):){1}\/{2}(?P<host>[^:=?/\s]+):?(?P<port>[0-9]*)(?P<path>\/?[^\s]*)'
rates_path = '/currencies/exchange_rates?symbols={symbols}'


def get_token(host: str, payload: dict) -> str | None:
    conn = http.client.HTTPSConnection(host)
    headers = {'content-type': 'application/json'}
    conn.request(
        'POST',
        '/oauth/token',
        json.dumps(payload),
        headers)
    res = conn.getresponse()
    if res.status == 200:
        return json.loads(res.read().decode('utf-8'))['access_token']
    else:
        return None


def get_rates(host: str, token: str, symbols: str) -> Response:
    conn = http.client.HTTPSConnection(host)
    headers = {'Authorization': f'Bearer {token}'}
    conn.request('GET', rates_path.format(symbols=symbols), None, headers)
    res = conn.getresponse()
    return {'status': res.status, 'json': json.loads(res.read().decode('utf-8'))}


def report_health(url: str) -> None:
    match = re.search(url_regex, url, re.IGNORECASE)
    if match is not None:
        conn = http.client.HTTPSConnection(match.group('host'))
        if match.group('port') is not None and match.group('port') != '':
            conn.port = int(match.group('port'))
        conn.request('GET', match.group('path'))
