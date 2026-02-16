import pytest
import uuid


def u(s: str) -> str:
    return f"{s}-{uuid.uuid4().hex[:8]}"

def email() -> str:
    return f"test-{uuid.uuid4().hex[:8]}@example.com"

def contact() -> str:

    return f"04{uuid.uuid4().int % 10_000_000_000:010d}"[:10]

RESOURCES = [
    ("/artists/",    lambda: {"name": u("Test Artist")},    lambda: {"name": u("Updated Artist")}, "name"),
    ("/writers/",    lambda: {"name": u("Test Writer")},    lambda: {"name": u("Updated Writer")}, "name"),
    ("/publishers/", lambda: {"name": u("Test Publisher")}, lambda: {"name": u("Updated Publisher")}, "name"),

    ("/costumers/",
     lambda: {"name": u("Test Costumer"), "email": email(), "contact": contact()},
     lambda: {"name": u("Updated Costumer"), "email": email(), "contact": contact()},
     "email"),
]

@pytest.mark.parametrize("collection,create_fn,update_fn,match_field", RESOURCES)
def test_basic_crud(crud, collection, create_fn, update_fn, match_field):
    create_payload = create_fn()
    rid = crud.create_id_by_list(collection, create_payload, match_field)

    crud.get_one(f"{collection}{rid}")
    crud.update(f"{collection}{rid}", update_fn())
    crud.list_all(collection)
    crud.delete(f"{collection}{rid}")
