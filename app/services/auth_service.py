from ..models import User
import bcrypt
from ..extensions import db
from sqlalchemy.orm.exc import NoResultFound


def encode(password: str) -> str:
    """Hash the password using bcrypt."""
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pass.decode('utf-8')


class AuthService():
    @staticmethod
    def register_user(email: str, password: str, username: str, first_name:str,
            last_name:str, file: dict = None):
        """Register a new user and save them to the database."""
        try:
            # Hash the user's password
            pswd = encode(password)
            
            # Set profile_img to the file URL if provided, else None
            profile_img = file if file else None

            # Create the User object
            user = User(
                email=email,
                password=pswd,
                username=username,
                profile_img=profile_img,
                first_name=first_name,
                last_name=last_name,
                cover='none'  # Either file URL or None
            )
            
            # Add user to the database session and commit
            db.session.add(user)
            db.session.commit()

            return user  # Return the user object if registration is successful
        
        except Exception as e:
            # Handle and log any exceptions (e.g., unique constraint violations)
            db.session.rollback()  # Roll back the session in case of error
            raise Exception(f"User registration failed: {str(e)}")

    @staticmethod
    def login(email: str, password: str) -> bool:
        try:
            # Correctly use filter() with a condition
            user = User.query.filter(User.email == email).one()
            isCorrect = bcrypt.checkpw(password.encode('utf-8'), user.password. encode('utf-8'))
            return isCorrect
        except NoResultFound:
            # Handle the case where no user was found
            return False