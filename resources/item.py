import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from db import items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="operations on items")

@blp.route("/item/<string:item_id>")
class Store(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return stores[item_id]
        except KeyError:
            abort(404, message="item not found.")

    def delete(self, item_id):
        try:
            del stores[item_id]
            return {"message": "item deleted."}
        except KeyError:
            abort(404, message="item not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="item not found.")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.arguments(201, ItemSchema)
    def post(self, item_data):
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