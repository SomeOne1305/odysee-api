import os
import base64
import uuid

from ..storage import Storage
from imagekitio.file import UploadFileRequestOptions
from ..extensions import db
from ..constants import VIDEO_FILE_TYPES, IMAGE_FILE_TYPES
from ..models import Video, Tag
from sqlalchemy import exists
from ..utils import is_valid_uuid

class VideoService:
    @staticmethod
    def upload_video(request, title: str, description: str, user_id: str, tags: list):
        # Проверка наличия файлов
        print(request.files)
        if "video" not in request.files:
            raise ValueError("Video is required!")
        if "thumbnail" not in request.files:
            raise ValueError("Thumbnail image for video is required!")

        # Обработка видео
        video_file = request.files['video']
        if video_file.filename == '':
            raise ValueError("No file selected for video")
        video_ext = os.path.splitext(video_file.filename)[1]
        if video_ext not in VIDEO_FILE_TYPES:
            raise ValueError(f"Unsupported file type {video_ext.replace('.', '').capitalize()} for video")

        # Обработка миниатюры
        thumbnail_file = request.files['thumbnail']
        if thumbnail_file.filename == '':
            raise ValueError("No file selected for thumbnail")
        thumbnail_ext = os.path.splitext(thumbnail_file.filename)[1]
        if thumbnail_ext not in IMAGE_FILE_TYPES:
            raise ValueError(f"Unsupported file type {thumbnail_ext.replace('.', '').capitalize()} for thumbnail")

        # Загрузка видео
        video_buffer = base64.b64encode(video_file.read())
        video_name = os.urandom(12).hex() + video_ext
        video = Storage.upload_file(
            file=video_buffer,
            file_name=video_name,
            options=UploadFileRequestOptions(folder="odysee/contents"),
        )
        video_info = {"fileId": video.file_id, "url": video.url}

        # Загрузка миниатюры
        thumbnail_buffer = base64.b64encode(thumbnail_file.read())
        thumbnail_name = os.urandom(12).hex() + thumbnail_ext
        thumbnail = Storage.upload_file(
            file=thumbnail_buffer,
            file_name=thumbnail_name,
            options=UploadFileRequestOptions(folder="odysee/contents/thumbnails"),
        )
        thumbnail_info = {"fileId": thumbnail.file_id, "url": thumbnail.url}

        # Получение тегов
        list_of_tags = Tag.query.filter(Tag.id.in_(tags)).all()
        found_tag_ids = {tag.id for tag in list_of_tags}
        requested_tag_ids = set(tags)
        missing_tag_ids = requested_tag_ids - found_tag_ids

        if missing_tag_ids:
            raise ValueError(f"Tags not found with IDs: {missing_tag_ids}")

        # Создание объекта Video
        video_data = Video(
            title=title,
            thumbnail=thumbnail_info,
            src=video_info,
            description=description,
            properties={
                "duration":video.response_metadata.raw['duration'],
                "height": video.response_metadata.raw['height'],
                "width": video.response_metadata.raw['width'],
            },
            views=0,
            user_id=user_id
        )
        video_data.tags.extend(list_of_tags)

        # Сохранение в базу данных
        db.session.add(video_data)
        db.session.commit()

        return video_data
    
    @staticmethod
    def get_all():
        contents = Video.query.all()
        return [{
            "id": content.id,
            "title": content.title,
            "description": content.description,
            "views": content.views,
            "src": content.src,
            "thumbnail": content.thumbnail,
            "tags": [{"id": str(tag.id), "title": tag.title} for tag in content.tags],
            "properties":{
                "duration":content.properties['duration'],
                "height": content.properties['height'],
                "width": content.properties['width'],
            },
            "created_at": content.created_at.isoformat() if content.created_at else None, 
            "updated_at": content.updated_at.isoformat() if content.updated_at else None,
            "user": {
                "username": content.user.username,  # Используем точечную нотацию
                "first_name": content.user.first_name,
                "last_name": content.user.last_name,
                "profile_img":content.user.profile_img
            }
        } for content in contents]

    @staticmethod
    def get_video_by_id(id:str):
        video = Video.query.get(id)
        if video:
            video.views = video.views + 1
            db.session.commit()
            return {
            "id": video.id,
            "title": video.title,
            "description": video.description,
            "views": video.views,
            "src": video.src,
            "thumbnail": video.thumbnail,
            "tags": [{"id": str(tag.id), "title": tag.title} for tag in video.tags],
            "created_at": video.created_at.isoformat() if video.created_at else None, 
            "updated_at": video.updated_at.isoformat() if video.updated_at else None,
            "duration":video.duration,
            "user": {
                "username": video.user.username,  # Используем точечную нотацию
                "first_name": video.user.first_name,
                "last_name": video.user.last_name,
                "profile_img":video.user.profile_img
            }
        }
    @staticmethod  
    def video_exists(id: str) -> bool:
        """Checks if a video with the given ID already exists in the database."""
        if not is_valid_uuid(id):
            return False
        vid = Video.query.get(id)
        if vid :
            return True
        else :
            return False

    @staticmethod
    def check_eligibility(user_id, content_id):
        """Checking video belongs to user """
        content = Video.query.get(content_id)
        if str(content.user.id) == str(user_id):
            return True
        else:
            return False

    @staticmethod
    def delete_content(content_id):
        content = Video.query.get(content_id)
        if content:
            Storage.delete_file(content.src['fileId'])
            Storage.delete_file(content.thumbnail["fileId"])

            db.session.delete(content)
            db.session.commit()