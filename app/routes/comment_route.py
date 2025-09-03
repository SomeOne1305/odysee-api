from flask import (Blueprint, request, jsonify, make_response)
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..schemas import CreateComment
from ..services import CommentService

comment_route = Blueprint('Comments', __name__)

@comment_route.route('/write/<string:id>', methods=["POST"])
@jwt_required()
def write_comment(id:str):
    user_id = get_jwt_identity()
    try:
        schema = CreateComment()
        data = schema.load(request.json)
        comment = CommentService.createComment(user_id,id, data)
        return jsonify({"message":"OK", "data":{
            "user_id": comment.user_id,
            "video_id":comment.video_id,
            "text":comment.text
        }}), 200
    except Exception as e:
        return make_response(
            jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 500
        )

@comment_route.route('/delete/<string:comment_id>', methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id):
    user_id = get_jwt_identity()  # Get the user ID from the JWT token

    try:
        # Check if the user is eligible to delete the comment
        is_eligible = CommentService.checking_user_eligibility(user_id, comment_id)
        if not is_eligible:
            return jsonify({"message": "Permission denied"}), 403

        # Attempt to delete the comment
        is_succeed = CommentService.delete_comment(comment_id)
        if is_succeed:
            return jsonify({"message": "Comment deleted successfully"}), 200
        else:
            return jsonify({"message": "Comment not found"}), 404

    except Exception as e:
        # Log the error for debugging
        print(f"Error deleting comment: {e}")
        return jsonify({"message": "An unexpected error occurred", "details": str(e)}), 500


@comment_route.route("/video/<string:video_id>", methods=["GET"])
def get_video_comments(video_id):
    try:
        if not CommentService.is_video_available(video_id):
            return make_response(jsonify({
                "message":f"Not found in video ID {video_id}"
            })), 404
        
        comments = CommentService.get_comments(video_id)
        return make_response(jsonify({
            "message":"OK",
            "data":comments
        }))
    except Exception as e:
        return make_response(
            jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 500
        )