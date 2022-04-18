import json as jsonlib
from typing import Optional
import uuid

import requests
import time
from django.conf import settings


class BackOffSession(requests.Session):
    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ):
        attempts = 10
        att = 0
        while att <= attempts:
            att += 1
            try:
                return super().request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    headers=headers,
                    cookies=cookies,
                    files=files,
                    auth=auth,
                    timeout=timeout,
                    allow_redirects=allow_redirects,
                    proxies=proxies,
                    hooks=hooks,
                    stream=stream,
                    verify=verify,
                    cert=cert,
                    json=json,
                )
            except requests.exceptions.ConnectionError:
                timeout = 2 ** att
                print(f"[BackOffSession]: ConnectionError. Retrying in {timeout}")
                time.sleep(timeout)
        raise requests.exceptions.ConnectionError("Backoff exceeded max number of attempts!")


class Flow(object):
    def __init__(self):
        self.endpoint = settings.FLOW_WALLLET_API_URL
        self.session = BackOffSession()

    def get_all_accounts(self) -> Optional[dict]:
        endpoint = self.endpoint + "accounts"
        resp = self.session.get(endpoint)
        if resp.status_code != 200:
            return None
        return jsonlib.loads(resp.content)

    def post_new_account(self):
        endpoint = self.endpoint + "accounts"
        headers = {'Idempotency-Key': str(uuid.uuid4())}
        resp = self.session.post(endpoint, headers=headers)
        if resp.status_code != 201:
            return None
        return jsonlib.loads(resp.content)

    def get_account_by_address(self, address: str) -> Optional[dict]:
        endpoint = self.endpoint + f"accounts/{address}"
        resp = self.session.get(endpoint)
        if resp.status_code != 200:
            return None
        return jsonlib.loads(resp.content)
