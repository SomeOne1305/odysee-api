from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from ..schemas import CreateTagScheme
from ..services import TagsService

tags_route = Blueprint("Tags", __name__)


@tags_route.route("/create", methods=["POST"])
def create():
    try:
        # Validate and deserialize the incoming request data
        schema = CreateTagScheme()
        data = schema.load(request.get_json())

        # Check if the tag already exists
        if TagsService.tag_exists(data['title']):
            return jsonify({"message": "Tag already exists"}), 400

        # Create the tag
        tag = TagsService.create_tag(data['title'])
        return jsonify({"message": "Tag created successfully", "data":{
            "id":str(tag.id),
            "title":tag.title
        }}), 201

    except ValidationError as err:
        # Handle validation errors
        return jsonify(err.messages), 400

    except Exception as e:
        # Handle all other exceptions
        return (
            jsonify({"error": "An unexpected error occurred", "message": str(e)}),
            500,
        )

@tags_route.route('/all', methods=["GET"])
def get_tags():
    try:
        tags = TagsService.get_all()
        return jsonify({
            'message':"Ready",
            "data":tags
        })
    except Exception as e:
        # Handle all other exceptions
        return (
            jsonify({"error": "An unexpected error occurred", "message": str(e)}),
            500,
        )
@tags_route.route("/edit/<string:tag_id>", methods=["PUT"])
def update_tag(tag_id:str):
    try:
        # Validate and deserialize the incoming request data
        schema = CreateTagScheme()
        data = schema.load(request.get_json())

        # Check if the tag exists
        tag = TagsService.get_tag_by_id(tag_id)
        if not tag:
            return jsonify({"message": "Tag not found"}), 404
        # Update the tag
        TagsService.update_tag(tag_id, data['title'])
        return jsonify({"message": "Tag updated successfully"}), 200

    except ValidationError as err:
        # Handle validation errors
        return jsonify(err.messages), 400

    except Exception as e:
        # Handle all other exceptions
        return (
            jsonify({"error": "An unexpected error occurred", "message": str(e)}),
            500,
        )

@tags_route.route('/delete/<string:tag_id>', methods=["DELETE"])
def delete_tag(tag_id):
    try:
        tag = TagsService.get_tag_by_id(tag_id)
        if not tag:
            return jsonify({"message": "Tag not found"}), 404
        TagsService.delete_tag(tag_id)
        return jsonify({"message":"Deleted successfully "}), 200
    except Exception as e:
        # Handle all other exceptions
        return (
            jsonify({"error": "An unexpected error occurred", "message": str(e)}),
            500,
        )
