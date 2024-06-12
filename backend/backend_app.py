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


def get_reversed(direction):
    return direction == "desc"


@app.route("/api/posts", methods=["GET", "POST"])
def get_posts():
    if not POSTS:
        return "POSTS is empty"

    if request.method == "POST":
        post = request.get_json()
        validation_result = validate_post_data(post)

        if validation_result is not True:
            return (
                jsonify(
                    {"error": f"Invalid post data, {validation_result} is "
                              f"missing"}
                ),
                400,
            )
        post["id"] = max((post.get("id", 0) for post in POSTS), default=0) + 1
        POSTS.append(post)
        return jsonify(post), 201

    sort_key = request.args.get("sort")
    direction = request.args.get("direction")

    if sort_key or direction:
        if sort_key in ["title", "content"] and direction in ["asc", "desc"]:
            sort_direction = get_reversed(direction)
            sorted_posts = sorted(
                POSTS, key=lambda blog_post: blog_post[sort_key],
                reverse=sort_direction
            )
            return jsonify(sorted_posts), 200
        else:
            return (
                jsonify(
                    {
                        "error": f"Invalid parameter sort should be 'title' "
                                 f"or 'content' and direction should be "
                                 f"'asc' or 'desc'"
                    }
                ),
                400,
            )

    return jsonify(POSTS), 200


def find_post(post_id):
    for post in POSTS:
        if post["id"] == post_id:
            return post


@app.route("/api/posts/<int:id>", methods=["PUT"])
def update_post(post_id):
    post = find_post(post_id)

    if post is None:
        return (
            jsonify({"error": f"Post with id {post_id} is not found."}),
            404,
        )

    new_post = request.get_json()
    post.update(new_post)
    return (
        jsonify(new_post),
        200,
    )


@app.route("/api/posts/<int:id>", methods=["DELETE"])
def delete_post(post_id):
    post = find_post(post_id)

    if post is None:
        return (
            jsonify({"error": f"Post with id {post_id} is not found."}),
            404,
        )

    POSTS.remove(post)
    return (
        jsonify({"message": f"Post with id {post_id} has been deleted " 
                            f"successfully."}),
        200,
    )


@app.route("/api/posts/search", methods=["GET"])
def search_post():
    searched_title = request.args.get("title")
    searched_content = request.args.get("content")
    filtered_posts = [
        post
        for post in POSTS
        if (searched_title and searched_title.lower() in post["title"].lower())
        or (searched_content and searched_content.lower() in
            post["content"].lower())
    ]

    if not filtered_posts:
        return jsonify([])
    return jsonify(filtered_posts), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
