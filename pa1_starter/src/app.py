import json

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

posts = {
    1 : {
      "id": 1,
      "upvotes": 1,
      "title": "My cat is the cutest!",
      "link": "https://i.imgur.com/jseZqNK.jpg",
      "username": "alicia98",
      "comments": [
        {
            "id": 1,
            "upvotes": 8,
            "text": "Wow my first Reddit gold!",
            "username": "alicia98"
        }
      ]
    }
}

posts_count = 2
comments_count = 2

@app.route("/api/posts/")
def get_task():
    """
    Sends GET request to server to retrieve all exists posts
    """
    res = {"posts": list(posts.values())}
    return json.dumps(res), 200

@app.route("/api/posts/", methods=["POST"])
def create_post():
    """
    Sends POST request to server and creates a new post with a JSON input
    """
    global posts_count

    body = json.loads(request.data) 
    title = body["title"]
    link = body["link"]
    username = body["username"]

    # New post object
    post = {"id": posts_count, "upvotes": 1, "title": title, 
            "link": link, "username": username, "comments":[]}

    posts[posts_count] = post

    # Increment post_count for ID tracking
    posts_count += 1

    return json.dumps(post), 201

@app.route("/api/posts/<int:post_id>/", methods=["GET"])
def get_post_id(post_id):
    """
    Sends GET request to server to post with post_id
    """
    post = posts.get(post_id)

    # Check if post exists
    if not post: 
        return json.dumps({"error": "Post not found"}), 404

    return json.dumps(post), 200  # Return post directly

@app.route("/api/posts/<int:post_id>/", methods=["DELETE"])
def delete_post_id(post_id):
    """
    Sends DELETE request to server to delete post of given ID post_id
    """
    post = posts.get(post_id)

    # Check if post exists
    if not post: 
        return json.dumps({"error": "Post not found"}), 404

    del posts[post_id]
    return json.dumps(post), 200 

@app.route("/api/posts/<int:post_id>/comments/")
def get_comment(post_id):
    """
    Sends GET request to server to retrieve all comments in post with post ID post_id
    """
    post = posts.get(post_id)
    if not post: 
        return json.dumps({"error": "Post not found"}), 404
    
    comments = post["comments"]
    return json.dumps({"comments": comments}), 200 

@app.route("/api/posts/<int:post_id>/comments/", methods=["POST"])
def comment_on_post(post_id):
    """
    Sends POST request to server to create a new comment for post with ID post_id
    """
    global comments_count

    # Check if post exists first
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post not found"}), 404

    body = json.loads(request.data)
    text = body["text"]
    username = body["username"]

    # Create new comment object
    comment = {"id": comments_count, "upvotes": 1, "text": text, "username": username}

    # Add comment to post
    comments = post["comments"]
    comments.append(comment)

    # Increment global comments_count to track ID
    comments_count += 1

    return json.dumps(comment), 201
    
@app.route("/api/posts/<int:post_id>/comments/<int:comment_id>/", methods=["POST"])
def edit_comment(post_id, comment_id):
    """
    Sends PUT request to server to update comment with comment ID comment_id in post post_id
    """
    # Check if post exists
    post = posts.get(post_id)
    if not post:
        return json.dumps({"error": "Post not found"}), 404
    
    body = json.loads(request.data)
    updated_text = body.get("text")
    
    if not updated_text:
        return json.dumps({"error": "Text field required"}), 400
    
    comments = post["comments"]
    
    # Find comment by id
    comment = None
    for c in comments:
        if c["id"] == comment_id:
            comment = c
            break
    
    if not comment:
        return json.dumps({"error": "Comment not found"}), 404
    
    comment["text"] = updated_text
    return json.dumps(comment), 200