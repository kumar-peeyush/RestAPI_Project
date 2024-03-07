import uuid
from flask_smorest import abort
from flask import Flask, request
from db import items, stores

app = Flask(__name__)

@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in the JSON payload."
        )
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message=f"Bad request. Ensure 'name' is included in the JSON payload.")
    store_id = uuid.uuid4().hex #sd89dvy9ssnv
    store = {**store_data, "id":store_id}
    stores[store_id] = store
    return store, 201

@app.get("/store/<string:store_id>")
def get_stores_names(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")

@app.post("/item")
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(400,
              message="Bad Request. Ensure 'price', 'store_id' and 'names' are included in JSON payload.")
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"Item already exists.")

    if item_data["store_id"] not in stores:
        abort(404, message="Store not found.")
    item_id = uuid.uuid4().hex  # sd89dvy9ssnv
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201

@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")


print("hello for github")
print("hello for github 2")
print("hello for github 3")