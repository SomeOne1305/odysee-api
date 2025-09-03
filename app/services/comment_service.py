from ..extensions import db
from ..models import Comment, User, Video
from sqlalchemy.orm import joinedload
import uuid

class CommentService:
    @staticmethod
    def createComment(user_id:str,video_id:str, data):
        comment = Comment(
            text = data['text'],
            video_id = video_id,
            user_id = user_id
        )
        db.session.add(comment)
        db.session.commit()
        return comment
    
    @staticmethod
    def is_user_available(id:str)-> bool:
        """Checking whether user is available"""
        user = User.query.get(id)
        if user:
            return True
        else:
            return False
        
    @staticmethod
    def is_video_available(id:str) -> bool:
        """Checking whether video is available"""
        video = Video.query.get(id)
        if video:
            return True
        else:
            return False
        
    @staticmethod
    def checking_user_eligibility(user_id: str, comment_id: str):
        """
        Check if the user is eligible to delete the comment.
        """
        try:
            # Fetch the comment with the user relationship loaded
            comment = Comment.query.options(joinedload(Comment.user)).filter_by(id=comment_id).first()

            if not comment:
                return False  # Comment does not exist

            # Convert user_id (string) to UUID object for comparison
            user_id_uuid = uuid.UUID(user_id.strip())  # Trim and convert to UUID

            print(f"user id: {user_id_uuid}")
            print(f"comment user id: {comment.user.id}")
            print(comment.user.id == user_id_uuid)  # Compare UUID objects

            # Check if the current user is the owner of the comment
            return comment.user.id == user_id_uuid

        except Exception as e:
            # Log the error for debugging
            print(f"Error checking user eligibility: {e}")
            return False



    @staticmethod 
    def get_comments(video_id:str)->list:
        comments = Comment.query.filter(Comment.video_id==video_id)
        return [{
            "id":comment.id,
            "text":comment.text,
            "user":{
                "id":comment.user.id,
                "first_name":comment.user.first_name,
                "last_name":comment.user.last_name,
                "profile_img":comment.user.profile_img
            },
            "created_at": comment.created_at.isoformat() if comment.created_at else None, 
                 } for comment in comments]

    @staticmethod
    def delete_comment(comment_id:str):
        comment = Comment.query.get(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return True
        return False