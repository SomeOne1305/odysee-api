from ..models import User
from ..storage import Storage
from ..extensions import db
from ..models import User

class UserService:
    @staticmethod
    def get_me(id: str):
        user = User.query.filter_by(id=id).first()
        user_data = None
        if user:
            user_data = {
                "id": str(user.id),  # Convert to string if UUID
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "profile_img": user.profile_img,  # Include only safe fields
                "cover": user.cover,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            }
            return user_data

    @staticmethod
    def upload_image(user_id:str, fileInfo:dict = None):
        user = User.query.get(user_id)
        user.profile_img = fileInfo
        db.session.commit()
        return user
    
    @staticmethod
    def delete_profile_img(user_id: str ,def_info:dict = None):
        user = User.query.get(user_id)
        user.profile_img = def_info
        db.session.commit()
        return user

    @staticmethod
    def delete_me(user):
        if user.videos:
            for video in user.videos:
                Storage.delete_file(video.src.id)
        if user.shorts:
            for shorts in user.shorts:
                Storage.delete_file(shorts.src.id)
