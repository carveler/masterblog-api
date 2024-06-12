from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_post_data(data):
    if "title" not in data:
        return "title"
    elif "content" not in data:
        return "content"
    return True


@app.route("/api/posts", methods=["GET", "POST"])
def get_posts():
    if request.method == "POST":
        post = request.get_json()
        if not validate_post_data(post) == True:
            return (
                jsonify(
                    {
                        "error": f"Invalid post data, {validate_post_data(post)} is missing"
                    }
                ),
                400,
            )
        post["id"] = max(post["id"] for post in POSTS) + 1
        POSTS.append(post)
        return jsonify(post), 201

    return jsonify(POSTS)


def find_post(id):
    for post in POSTS:
        if post["id"] == id:
            return post


@app.route("/api/posts/<int:id>", methods=["PUT"])
def update_post(id):
    post = find_post(id)

    if post is None:
        return (
            jsonify({"error": f"Post with id {id} is not found."}),
            404,
        )

    new_post = request.get_json()
    post.update(new_post)
    return (
        jsonify(new_post),
        200,
    )


@app.route("/api/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    post = find_post(id)

    if post is None:
        return (
            jsonify({"error": f"Post with id {id} is not found."}),
            404,
        )

    POSTS.remove(post)
    return (
            jsonify({"message": f"Post with id {id} has been deleted successfully."}),
            200,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
