from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from ..schemas import CreateContentSchema
from ..services import VideoService
from ..exceptions import NotFoundError

video_route = Blueprint("Video", __name__)

@video_route.route('/upload', methods=["POST"])
@jwt_required()
def upload_content():
    user_id = get_jwt_identity()
    try:
        # Получаем данные из form-data
        form_data = request.form.to_dict()
        form_data['tags'] = request.form.getlist('tags')

        # Валидируем данные с помощью схемы
        schema = CreateContentSchema()
        validated_data = schema.load(form_data)

        # Извлекаем валидированные данные
        title = validated_data['title']
        description = validated_data['description']
        tags = validated_data['tags']

        # Загружаем видео с помощью сервиса
        video = VideoService.upload_video(request, title, description, user_id, tags)

        return jsonify({
            'message': "Video is created",
            'data': {
                "id": str(video.id),
                "title": video.title,
                "description": video.description,
                "src": video.src,
                "thumbnail": video.thumbnail,
                "tags": [{"id": str(tag.id), "title": tag.title} for tag in video.tags],
                "created_at": video.created_at.isoformat() if video.created_at else None,
                "updated_at": video.updated_at.isoformat() if video.updated_at else None,
                "properties": {
                    "duration": video.properties['duration'],
                    "height": video.properties['height'],
                    "width": video.properties['width'],
                },
            }
        }), 200

    except ValidationError as err:
        return jsonify(err.messages), 400

    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    except Exception as e:
        return jsonify({"message": "An unexpected error occurred", "error": str(e)}), 500
    

@video_route.route('/all',methods=["GET"])
def get_all_contents():
    try:
        videos = VideoService.get_all()
        return jsonify({
            'message':"Ready",
            "data":videos
        })
    except Exception as e:
        # Handle all other exceptions
        return (
            jsonify({"error": "An unexpected error occurred", "message": str(e)}),
            500,
        )
@video_route.route('/video/<string:video_id>')
def get_video(video_id):
    try:
        # Проверяем, существует ли видео
        if not VideoService.video_exists(video_id):
            raise NotFoundError(f"Content is not found with ID {video_id}")

        # Получаем видео по ID
        content = VideoService.get_video_by_id(video_id)
        return jsonify({
            "message": "Ready",
            "data": content
        }), 200

    except NotFoundError as e:
        # Обработка ошибки "Не найдено"
        return jsonify({"message": str(e)}), 404

    except Exception as e:
        # Обработка всех остальных ошибок
        return jsonify({
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500

@video_route.route('/delete/<string:video_id>', methods=["DELETE"])
@jwt_required()
def delete_video(video_id):
    user_id = get_jwt_identity()
    try:
        if not VideoService.video_exists(video_id):
            raise NotFoundError(f"Content is not found with ID {video_id}")
        if not VideoService.check_eligibility(user_id, video_id):
            return jsonify({"message":"Forbidden"}), 403
            
        VideoService.delete_content(video_id)
        return jsonify({
            "message":f"Content with ID {video_id} deleted !"
        }), 200
        return 0
    except Exception as e:
        return jsonify({
            "message": "An unexpected error occurred",
            "error": str(e)
        }), 500