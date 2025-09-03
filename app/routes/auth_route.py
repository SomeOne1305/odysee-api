from marshmallow import ValidationError
from flask import Blueprint, request, jsonify, make_response
import uuid
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    jwt_required,
    get_jwt_identity,
    unset_jwt_cookies,
)
from flask_mail import Message
from ..schemas import RegisterSchema, VerifySchema, CreateUserSchema, LoginUserSchema
from ..models import User
from ..extensions import CacheStorage, mailer
from ..constants import IMAGE_FILE_TYPES
from ..storage import Storage
from ..services import AuthService
from ..utils import template_mail
from imagekitio.file import UploadFileRequestOptions
from ..lib.utils import return_decoded_value
import app
import os
import base64
import datetime

# Create the Blueprint
auth_route = Blueprint("Auth", __name__)


@auth_route.route("/register", methods=["POST"])
def register():
    """Register Route"""
    try:
        schema = RegisterSchema()
        data = schema.load(request.get_json())
        email: str = data["email"]
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            return jsonify({"message": "This user is already registered !"}), 403
        token = uuid.uuid1().hex
        CacheStorage.set(f"token:{token}", email, ex=600)
        message = Message(
            subject="Please, verify your email to activate your account",
            recipients=[email],
            body=token,
            html=template_mail(token=token)
        )
        mailer.send(message)
        return jsonify({"message": f"code is sent to {email}"}), 200
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        # Handle all other exceptions
        return (
            jsonify({"error": "An unexpected error occurred", "message": str(e)}),
            500,
        )


@auth_route.route("/verify", methods=["POST"])
def verifyUser():
    """Verify User"""
    try:
        schema = VerifySchema()
        data = schema.load(request.get_json())
        email = data["email"]
        token = data["token"]
        key = return_decoded_value(f"token:{token}")

        print(key, token)
        if email != key:
            return (
                jsonify(
                    {"passed": False, "message": "Invalid or expired verification !"}
                ),
                403,
            )
        else:
            new_verified_token = uuid.uuid1().hex
            CacheStorage.delete(f"token:{token}")
            CacheStorage.set(email, new_verified_token, ex=600)
            return jsonify(
                {
                    "passed": True,
                    "registry_token": new_verified_token,
                    "message": "Verification is passed",
                }
            )
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        # Handle all other exceptions
        return (
            jsonify({"error": "An unexpected error occurred", "message": str(e)}),
            500,
        )

@auth_route.route("/create", methods=["POST"])
def createUser():
    """Create verified user"""
    res = None  # Initialize res to None at the beginning
    try:
        # Validating request body
        schema = CreateUserSchema()
        data = schema.load(request.form)

        # Debugging: Print the data to verify its contents
        print(data)

        # Extracting values from validated body
        email = data["email"]
        token = data["token"]
        username = data["username"]
        password = data["password"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        profile_img = data.get("profile_img")  # Optional field, use .get() to avoid KeyError

        # Validate the token
        if token != return_decoded_value(email):
            return (
                jsonify(
                    {
                        "message": "Registering process was broken due to token which is expired or invalid"
                    }
                ),
                400,
            )

        file_info = None  # Default to None when no file is uploaded

        # Check if a file was uploaded
        if "profile_img" in request.files:
            file = request.files["profile_img"]

            if file.filename == "":
                return jsonify({"error": "No selected profile image"}), 400

            ext_name = os.path.splitext(file.filename)[1]
            if ext_name not in IMAGE_FILE_TYPES:
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

            res = Storage.upload_file(
                file=file_buffer,
                file_name=random_name,
                options=UploadFileRequestOptions(folder="odysee/user"),
            )
            file_info = {"fileId": res.file_id, "url": res.url, "is_default": False}

        # Register the user with or without the file
        user = AuthService.register_user(
            email=email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            file=file_info,
        )

        # Prepare user data for response
        user_data = {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile_img": user.profile_img,
            "cover": user.cover,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
        }

        return jsonify(user_data), 201  # Return user data with a 201 Created status

    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        # Handle all other exceptions
        if res:  # Only attempt to delete the file if res was defined
            Storage.delete_file(res.file_id)
        return (
            jsonify({"error": "An unexpected error occurred", "message": str(e)}),
            500,
        )

@auth_route.route("/login", methods=["POST"])
def login_user():
    try:
        schema = LoginUserSchema()
        data = schema.load(request.json)
        email, password = data.values()

        # Check if the user exists and if credentials are valid
        isExist = User.query.filter_by(email=email).first()
        isAccessed = AuthService.login(email, password)

        if isExist and isAccessed:
            # Create access and refresh tokens
            access_token = create_access_token(
                identity=isExist.id, expires_delta=datetime.timedelta(minutes=15)
            )
            refresh_token = create_refresh_token(
                identity=isExist.id, expires_delta=datetime.timedelta(days=7)
            )

            # Create response
            resp = make_response(jsonify({"message": "Login successful"}))

            # Set both access and refresh tokens in HttpOnly cookies with proper max_age
            set_access_cookies(
                resp, access_token, max_age=15 * 60
            )  # Set to 15 minutes in seconds
            set_refresh_cookies(
                resp, refresh_token, max_age=7 * 24 * 60 * 60
            )  # Set to 7 days in seconds

            return resp
        return jsonify({"message": "Password or email is incorrect"}), 401

    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "message": str(e)}),
            500,
        )


@auth_route.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(
        identity=current_user, expires_delta=datetime.timedelta(minutes=15)
    )

    resp = make_response(jsonify({"message": "Token refreshed"}))
    set_access_cookies(resp, new_access_token, 15 * 60)
    return resp


@auth_route.route("/logout", methods=["POST"])
@jwt_required(refresh=True)
def logout():
    resp = make_response(jsonify({"message": "Successfully logged out"}))
    unset_jwt_cookies(resp)  # Use Flask-JWT-Extended helper
    return resp


@auth_route.route("/status", methods=["GET"])
def check_auth():
    status = False
    if "refresh_token_cookie" in request.cookies:
        status = True
    return make_response(jsonify({"status": status}))
