from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from uuid import UUID
from ..services import ReactionsService
from ..extensions import db

reaction_route = Blueprint("reaction", __name__)

@reaction_route.route("/like/<string:video_id>", methods=["POST"])
@jwt_required()
def toggle_like(video_id: str):
    """
    Toggle like for a video.
    """
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    try:
        video_id_uuid = UUID(video_id)  # Convert video_id to UUID
        user_id_uuid = UUID(user_id)  # Convert user_id to UUID

        result = ReactionsService.toggle_like(db.session, video_id_uuid, user_id_uuid)
        if "error" in result:
            return jsonify(result), 400

        return jsonify(result), 200

    except ValueError:
        return jsonify({"message": "Invalid video ID"}), 400
    except Exception as e:
        return jsonify({"message": "An error occurred", "details": str(e)}), 500
    
@reaction_route.route("/dislike/<string:video_id>", methods=["POST"])
@jwt_required()
def toggle_dislike(video_id: str):
    """
    Toggle dislike for a video.
    """
    user_id = get_jwt_identity()  # Get the user ID from the JWT token
    try:
        video_id_uuid = UUID(video_id)  # Convert video_id to UUID
        user_id_uuid = UUID(user_id)  # Convert user_id to UUID

        result = ReactionsService.toggle_dislike(db.session, video_id_uuid, user_id_uuid)
        if "error" in result:
            return jsonify(result), 400

        return jsonify(result), 200

    except ValueError:
        return jsonify({"message": "Invalid video ID"}), 400
    except Exception as e:
        return jsonify({"message": "An error occurred", "details": str(e)}), 500

@reaction_route.route("/likes/<string:video_id>", methods=["GET"])
def get_liked_and_disliked_users(video_id: str):
    """
    Get the count of likes and dislikes for a video,
    and whether the current user has liked or disliked it (if authenticated).
    """
    try:
        video_id_uuid = UUID(video_id)  # Convert video_id to UUID

        # Extract user_id from JWT token in cookie (if available)
        user_id = None
        jwt_token = request.cookies.get("refresh_token_cookie")  # Replace with your cookie name

        if jwt_token:
            try:
                # Decode the JWT token to get the user ID
                from flask_jwt_extended import decode_token
                decoded_token = decode_token(jwt_token)
                user_id = decoded_token["sub"]  # Assuming "sub" contains the user ID
                user_id = UUID(user_id)  # Convert user_id to UUID
            except Exception as e:
                print(f"Error decoding JWT token: {e}")
                # If the JWT token is invalid, treat the user as unauthenticated
                user_id = None

        result = ReactionsService.get_liked_and_disliked_users(db.session, video_id_uuid, user_id)
        if "error" in result:
            return jsonify(result), 404

        return jsonify(result), 200

    except ValueError:
        return jsonify({"message": "Invalid video ID"}), 400
    except Exception as e:
        return jsonify({"message": "An error occurred", "details": str(e)}), 500