import pytest
import uuid


def u(s: str) -> str:
    return f"{s}-{uuid.uuid4().hex[:8]}"

def test_comics_publisher(crud):
    pub_payload = {"name": u("Publisher for Comic")}
    pub_id = crud.create_id_by_list("/publishers/", pub_payload, "name")

    comic_payload = {
        "title": u("Test Comic"),
        "price": 9.99,
        "publisher_id": pub_id,
    }
    comic_id = crud.create_id_by_list("/comics/", comic_payload, "title")

    crud.get_one(f"/comics/{comic_id}")
    crud.list_all("/comics/")
    crud.update(f"/comics/{comic_id}", {"title": u("Updated Comic"), "price": 12.50})
    crud.delete(f"/comics/{comic_id}")
    crud.delete(f"/publishers/{pub_id}")
