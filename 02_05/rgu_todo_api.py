from flask import Flask, jsonify, request

app = Flask(__name__)

# Create to_do list
todos = [
    {"id": 1, "task": "Learn Flask", "done": False},
    {"id": 2, "task": "Build a REST API", "done": False},
    {"id": 3, "task": "Test the API", "done": False},
    {"id": 4, "task": "Watch another course from Kesha", "done": False},
]


@app.route("/")
def hello_world():
    return "<p>Welcome to your to-do list my dear!</p>"


# Helper function to create a new to-do item
@app.route("/todos", methods=["POST"])
def create_todo_entry():
    data = request.json
    if not data or "task" not in data:
        return jsonify({"error": "Task description is required"}), 400

    new_todo = {
        "id": (
            max(todo["id"] for todo in todos) + 1 if todos else 1
        ),  # Auto-increment ID
        "task": data["task"],
        "done": data.get("done", False),  # Default done status is False
    }
    todos.append(new_todo)
    return jsonify({"message": "To-do item created", "todo": new_todo}), 201


# Helper fucntion to return all to-do items
@app.route("/todos/all", methods=["GET"])
def get_all_todos():
    return jsonify(todos), 200


# Helper function to return a specific to-do item
@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo_entry(todo_id):
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo:
        return jsonify(todo), 200
    return jsonify({"error": "To-do item not found"}), 404


# Helper function to update a specific to-do item
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo_entry(todo_id):
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo:
        data = request.json
        todo["task"] = data.get("task", todo["task"])
        todo["done"] = data.get("done", todo["done"])
        return jsonify({"message": "To-do item updated", "todo": todo}), 200
    return jsonify({"error": "To-do item not found"}), 404


# Helper function to delete a specific to-do item
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo_entry(todo_id):
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]
    return jsonify({"message": f"To-do item with ID {todo_id} deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
