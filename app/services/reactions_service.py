from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
from ..models import Video, User

class ReactionsService:
    @staticmethod
    def toggle_like(db: Session, video_id: UUID, user_id: UUID) -> dict:
        """
        Toggle like for a video.
        If the user already liked the video, remove the like.
        If the user disliked the video, remove the dislike and add a like.
        """
        try:
            video = db.query(Video).filter(Video.id == video_id).first()
            user = db.query(User).filter(User.id == user_id).first()

            if not video or not user:
                return {"error": "Video or user not found"}

            if user in video.liked_by:
                # User already liked the video, so remove the like
                video.liked_by.remove(user)
                db.commit()
                return {"message": "Like removed", "liked": False}

            # Remove user from disliked_by (if present)
            if user in video.disliked_by:
                video.disliked_by.remove(user)

            # Add user to liked_by
            video.liked_by.append(user)
            db.commit()
            return {"message": "Video liked", "liked": True}

        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error toggling like: {e}")
            return {"error": "An error occurred"}

    @staticmethod
    def toggle_dislike(db: Session, video_id: UUID, user_id: UUID) -> dict:
        """
        Toggle dislike for a video.
        If the user already disliked the video, remove the dislike.
        If the user liked the video, remove the like and add a dislike.
        """
        try:
            video = db.query(Video).filter(Video.id == video_id).first()
            user = db.query(User).filter(User.id == user_id).first()

            if not video or not user:
                return {"error": "Video or user not found"}

            if user in video.disliked_by:
                # User already disliked the video, so remove the dislike
                video.disliked_by.remove(user)
                db.commit()
                return {"message": "Dislike removed", "disliked": False}

            # Remove user from liked_by (if present)
            if user in video.liked_by:
                video.liked_by.remove(user)

            # Add user to disliked_by
            video.disliked_by.append(user)
            db.commit()
            return {"message": "Video disliked", "disliked": True}

        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error toggling dislike: {e}")
            return {"error": "An error occurred"}
        
    @staticmethod
    def get_liked_and_disliked_users(db: Session, video_id: UUID, user_id: UUID = None) -> dict:
        """
        Get the count of likes and dislikes for a video,
        and whether the current user has liked or disliked it (if authenticated).
        """
        try:
            video = db.query(Video).filter(Video.id == video_id).first()
            if not video:
                return {"error": "Video not found"}

            # Get the count of likes and dislikes
            liked_users_count = len(video.liked_by)
            disliked_users_count = len(video.disliked_by)

            # Check if the current user has liked or disliked the video (if authenticated)
            user_has_liked = False
            user_has_disliked = False

            if user_id:
                user_has_liked = any(user.id == user_id for user in video.liked_by)
                user_has_disliked = any(user.id == user_id for user in video.disliked_by)

            return {
                "liked_users_count": liked_users_count,
                "disliked_users_count": disliked_users_count,
                "user_has_liked": user_has_liked,
                "user_has_disliked": user_has_disliked
            }

        except SQLAlchemyError as e:
            print(f"Error fetching liked/disliked users: {e}")
            return {"error": "An error occurred"}