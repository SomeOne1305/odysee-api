from flask import Blueprint, make_response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from sqlalchemy.inspection import inspect
from ..models import User
from sqlalchemy.exc import SQLAlchemyError
from ..services import UserService
from ..schemas import UpdateUserSchema
from ..extensions import db
from ..utils import serialize_data
from ..storage import Storage
import os
import base64
from imagekitio.file import UploadFileRequestOptions
user_route = Blueprint("User", __name__)

@user_route.route("/me", methods=["GET"])
@jwt_required()
def get_user():
    """Get the currently authenticated user's details."""
    try:
        # Retrieve the currently authenticated user's identity
        current_user_identity = get_jwt_identity()

        # Query the database for the user's details
        user_data = UserService.get_me(current_user_identity)
        # Handle cases where the user is not found
        if not user_data:
            return make_response(
                jsonify(
                    {
                        "message": "User not found.",
                        "error": "Invalid or missing user identity.",
                    }
                ),
                404,
            )

        # Prepare the response with user details

        return make_response(
            jsonify({"message": "User retrieved successfully.", "data": user_data}), 200
        )

    except SQLAlchemyError as db_error:
        # Handle database-related errors gracefully
        return make_response(
            jsonify({"error": "Database error occurred.", "details": str(db_error)}),
            500,
        )

    except Exception as e:
        # Handle unexpected errors
        return make_response(
            jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
        )


@user_route.route("/update-me", methods=["PUT"])
@jwt_required()
def update_user():
    user_identity = get_jwt_identity()
    user = User.query.get({"id": user_identity})
    if not user:
        return jsonify({"message": "User not found"}), 404
    try:
        schema = UpdateUserSchema()
        data = schema.load(request.get_json(), many=False)
        print(data)
        # Update user fields if provided in the request
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]
        if "cover" in data:
            user.cover = data["cover"]

        # Commit changes to the database
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "User updated successfully",
                    "data": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "cover": user.cover,
                    },
                }
            ),
            200,
        )
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    except SQLAlchemyError as db_error:
        # Handle database-related errors gracefully
        return make_response(
            jsonify({"error": "Database error occurred.", "details": str(db_error)}),
            500,
        )

    except Exception as e:
        # Handle unexpected errors
        return make_response(
            jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
        )


@user_route.route('/upload-profile', methods=["POST"])
@jwt_required()
def upload_profile_img():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return (
            make_response({"message": f"User is not found with ID ${user_id}"}),
            404,
        )
    
    file_info = None
    try:
        if "profile_img" not in request.files:
            return jsonify({"error": "No profile image provided"}), 400

        file = request.files["profile_img"]

        if file.filename == "":
            return jsonify({"error": "No selected profile image"}), 400

        ext_name = os.path.splitext(file.filename)[1]
        if ext_name not in [".png", ".jpeg", ".jpg", ".webp"]:
            return (
                jsonify(
                    {
                        "message": f"Unsupported file type {ext_name.replace('.', '').capitalize()}"
                    }
                ),
                400,
            )

        # Read the file buffer
        file_buffer = base64.b64encode(file.read())
        random_name = os.urandom(12).hex() + ext_name

        # Upload the file to the storage server
        res = Storage.upload_file(
            file=file_buffer,
            file_name=random_name,
            options=UploadFileRequestOptions(folder="odysee/user"),
        )
        file_info = {"fileId": res.file_id, "url": res.url, "is_default": False}

        # Check if the current profile image is not default before deleting
        if user.profile_img and not user.profile_img.get("is_default", True):
            try:
                # Verify that the file exists before attempting to delete it
                Storage.file.get_file_version_details(user.profile_img["fileId"])  # Check if the file exists
                Storage.delete_file(user.profile_img["fileId"])  # Delete the file
            except Exception as e:
                # Log the error but continue with the update
                print(f"Error deleting file: {e}")

        # Update user info in the database
        res = UserService.upload_image(user_id, file_info)
        user_data = {
            "id": str(res.id),  # Convert UUID to string if necessary    
            "profile_img": res.profile_img,  # Ensure this is a dictionary
        }
        return jsonify({
            "message": "Profile image is updated",
            "user": user_data
        })

    except SQLAlchemyError as db_error:
        # Handle database-related errors gracefully
        if file_info is not None:
            try:
                Storage.delete_file(file_info["fileId"])  # Clean up the uploaded file
            except Exception as e:
                print(f"Error deleting file during cleanup: {e}")
        return make_response(
            jsonify({"error": "Database error occurred.", "details": str(db_error)}),
            500,
        )
    except Exception as e:
        if file_info is not None:
            try:
                Storage.delete_file(file_info["fileId"])  # Clean up the uploaded file
            except Exception as cleanup_error:
                print(f"Error deleting file during cleanup: {cleanup_error}")
        # Handle unexpected errors
        return make_response(
            jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
        )
@user_route.route('/delete-profile-img',methods=["DELETE"])
@jwt_required()
def delete_profile_img():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    try:
        default_file = {"fileId": 'default_file_id', "url": 'default_img_url', "is_default": True}
        if user.profile_img['is_default'] is True:
            return jsonify({
                "message":"Unable to delete default image"
            }),400
        Storage.delete_file(user.profile_img['fileId'])
        res = UserService.delete_profile_img(user_id, default_file)
        user_data = {
                "id": str(res.id),  # Convert UUID to string if necessary    
                "profile_img": res.profile_img,  # Ensure this is a dictionary
                }
        return jsonify({
                "message": "Profile image is deleted",
                "user": user_data
            })
        
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    except SQLAlchemyError as db_error:
        # Handle database-related errors gracefully
        return make_response(
            jsonify({"error": "Database error occurred.", "details": str(db_error)}),
            500,
        )

    except Exception as e:
        # Handle unexpected errors
        return make_response(
            jsonify({"error": "An unexpected error occurred.", "details": str(e)}), 500
        )

@user_route.route("/delete-me", methods=["DELETE"])
@jwt_required()
def delete_me():

    user_identity = get_jwt_identity()
    user = User.query.get(user_identity)
    if not user:
        return (
            make_response({"message": f"User is not found with ID ${user_identity}"}),
            404,
        )
    data = serialize_data(user)
    print(data)
    return make_response({"message": "Deleted succcesfully !"})
