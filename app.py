from flask import Flask, jsonify, request

app = Flask(__name__)

items = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Mouse", "price": 29.99}
]

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items), 200

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((i for i in items if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200

@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json(force=True)
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Missing 'name' or 'price'"}), 400
    new_id = max(i["id"] for i in items) + 1 if items else 1
    new_item = {"id": new_id, "name": data["name"], "price": data["price"]}
    items.append(new_item)
    return jsonify(new_item), 201

@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = next((i for i in items if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    data = request.get_json(force=True)
    item["name"] = data.get("name", item["name"])
    item["price"] = data.get("price", item["price"])
    return jsonify(item), 200

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global items
    item = next((i for i in items if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    items = [i for i in items if i["id"] != item_id]
    return jsonify({"message": "Deleted", "item": item}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
