import os
import requests
import pytest
import time


def wait_till_api_is_ready(base_url: str, timeout_s: int = 30) -> None:
    deadline = time.time() + timeout_s
    last_err = None

    while time.time() < deadline:
        try:
            r = requests.get(f'{base_url}/health', timeout=3)
            if r.status_code == 200:
                return
        except Exception as e:
            last_err = e
        time.sleep(1)

    raise RuntimeError(f'API not ready at {base_url}. Error: {last_err}')


def get_id(payload: dict) -> int:
    candidates = [
        "id",
        "artist_id",
        "writer_id",
        "publisher_id",
        "comic_id",
        "costumer_id",
        "order_id",
        "order_comic_id",
    ]
    for k in candidates:
        v = payload.get(k)
        if isinstance(v,int):
            return v
    raise AssertionError(f"Could not find an Id.")
    


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "http://localhost:8080").rstrip("/")


@pytest.fixture(scope="session", autouse=True)
def api_is_ready(base_url: str):
    wait_till_api_is_ready(base_url)
    yield


@pytest.fixture
def http(base_url:str):
    class Client:
        def request(self,method: str, path: str, **kw):
            return requests.request(method, base_url + path, timeout=8, **kw)
        
        def get(self, path: str, **kw):    return self.request("GET", path, **kw)
        def post(self, path: str, **kw):   return self.request("POST", path, **kw)
        def patch(self, path: str, **kw):  return self.request("PATCH", path, **kw)
        def put(self, path: str, **kw):    return self.request("PUT", path, **kw)
        def delete(self, path: str, **kw): return self.request("DELETE", path, **kw)

    return Client()
        


@pytest.fixture
def crud(http):
    class CRUD:
        def create(self, collection: str, payload: dict) -> dict:
            r = http.post(collection, json=payload)
            if r.status_code not in (200,201):
                raise AssertionError(f"Create {collection} failed. Status ={r.status_code} body={r.text}")
            
            return r.json() if r.content else {}
        

        def get_one(self, item_url: str) -> dict:
            r = http.get(item_url)
            if r.status_code !=200:
                raise AssertionError(f"Get {item_url} failed. Status={r.status_code} body={r.text}")
        
            return r.json() if r.content else {}
        

        def list_all(self,collection: str):
            r = http.get(collection)
            if r.status_code != 200:
                raise AssertionError(f"List {collection} failed. Status={r.status_code} body={r.text}")
            return r.json() if r.content else None
        

        def update(self, item_url: str, payload: dict):
            r = http.patch(item_url, json=payload)
            if r.status_code == 405:
                r = http.put(item_url, json=payload)
            if r.status_code not in (200,204):
                raise AssertionError(f"Update {item_url} failed. Status={r.status_code} body={r.text}")
            return r
        

        def delete(self,item_url: str):
            r = http.delete(item_url)
            if r.status_code not in (200, 204):
                raise AssertionError(f"Delete {item_url} failed. Status={r.status_code} body={r.text}")
            return r
        

        def find_id(self, collection: str, match_field: str, match_value, id_field_candidates):
            data = self.list_all(collection)

            if isinstance(data, dict):
                for key in ("items", "data", "results"):
                    if isinstance(data.get(key), list):
                        data = data[key]
                        break

            if not isinstance(data, list):
                raise AssertionError(f"List response was not a list for {collection} Response: {data}")
            
            for item in data:
                if isinstance(item, dict) and item.get(match_field) == match_value:
                    for k in id_field_candidates:
                        v = item.get(k)
                        if isinstance(v,int):
                            return v
                    raise AssertionError(f"MAtched item has no Id. Item={item}")
            
            raise AssertionError(f"Could not find item in list for {collection} where {match_field}={match_value}. List={data}")
        

        def create_id_by_list(self, collection: str, payload: dict, match_field: str, id_candidates=None) -> int:
            self.create(collection, payload)
            if id_candidates is None:
                id_candidates = [
                    "id",
                    "artist_id",
                    "writer_id",
                    "publisher_id",
                    "comic_id",
                    "costumer_id",
                    "order_id",
                    "order_comic_id"
                ]

            return self.find_id(collection, match_field, payload[match_field], id_candidates)
    return CRUD()

