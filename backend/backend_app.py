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
                    {"error": f"Invalid post data, {validate_post_data(post)} is missing"}
                ),
                400,
            )
        post["id"] = max(post["id"] for post in POSTS) + 1
        POSTS.append(post)
        return jsonify(post), 201

    return jsonify(POSTS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
