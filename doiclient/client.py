import json
from future.moves.urllib.parse import urljoin

import requests


def json_dumps(data):
    return json.dumps({k: v for (k, v) in data.items() if v is not None})


def handle_error(resp):
    if 400 <= resp.status_code < 600:
        try:
            json = resp.json()
            resp.reason = json["error"]
        except:
            pass
        finally:
            resp.raise_for_status()


class DOIClient(object):

    def __init__(self, baseurl, version="v0", auth=None):
        self.auth = auth
        self.url = baseurl
        self.version = version

    def url_for(self, *path):
        return urljoin(self.url, "/".join(path))

    def check_status(self):
        """Check that the API we are trying to communicate with is online"""
        resp = requests.get(self.url + '/index')
        handle_error(resp)

    def get(self, did):
        """Return a document object corresponding to a single did"""
        try:
            headers = {'Accept' : 'application/vnd.citationstyles.csl+json'}
            response = self._get(did, headers=headers)
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            else:
                print("Exception!!" + str(e.reason))
                return None
        try:
            return Document(self, did, json=response.json())
        except ValueError as e:
            return None

    def _get(self, *path, **kwargs):
        resp = requests.get(self.url_for(*path), timeout=5, **kwargs)
        handle_error(resp)
        return resp

    def _post(self, *path, **kwargs):
        resp = requests.post(self.url_for(*path), **kwargs)
        handle_error(resp)
        return resp

    def _put(self, *path, **kwargs):
        resp = requests.put(self.url_for(*path), **kwargs)
        handle_error(resp)
        return resp

    def _delete(self, *path, **kwargs):
        resp = requests.delete(self.url_for(*path), **kwargs)
        handle_error(resp)
        return resp


class DocumentDeletedError(Exception):
    pass


class Document(object):

    def __init__(self, client, did, json=None):
        self.client = client
        self.did = did
        self.urls = None
        self.sha1 = None
        self._fetched = False
        self.refresh(json)

    def _render(self, include_rev=True):
        if not self._fetched:
            raise RuntimeError("Document must be fetched from server with doc.refresh() before being rendered as json")
        json = {
            "urls": self.urls,
            "hashes": self.hashes,
            "size": self.size
        }
        if include_rev:
            json["rev"] = self.rev
        return json

    def to_json(self, include_rev=True):
        json = self._render(include_rev=include_rev)
        json["did"] = self.did
        return json

    def refresh(self, json=None):
        """refresh the document contents from the server"""
        json = json or self.client._get(self.did).json()
        assert json["DOI"].lower() == self.did.lower()
        self.urls = [x['URL'] for x in json['link']]
        self.rev = ""
        self.size = ""
        self.hashes = ""
        self._fetched = True
