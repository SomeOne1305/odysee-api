import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .extensions import db

# Association tables for many-to-many relationships
user_liked_videos = Table(
    "user_liked_videos",
    db.Model.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True),
    Column("video_id", UUID(as_uuid=True), ForeignKey("video.id"), primary_key=True),
)

user_disliked_videos = Table(
    "user_disliked_videos",
    db.Model.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True),
    Column("video_id", UUID(as_uuid=True), ForeignKey("video.id"), primary_key=True),
)

video_tags = Table(
    "video_tags",
    db.Model.metadata,
    Column("video_id", UUID(as_uuid=True), ForeignKey("video.id"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tag.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "user"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # Automatically generate UUID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    email = Column(String(80), unique=True, nullable=False)
    username = Column(String(45), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    cover = Column(String, nullable=False)
    profile_img = Column(JSON, nullable=True)
    first_name = Column(String(40), nullable=False)
    last_name = Column(String(40), nullable=False)

    videos = relationship("Video", back_populates="user", cascade="all, delete-orphan")
    shorts = relationship("Short", back_populates="user", cascade="all, delete-orphan")
    liked_videos = relationship(
        "Video", secondary=user_liked_videos, back_populates="liked_by"
    )
    disliked_videos = relationship(
        "Video", secondary=user_disliked_videos, back_populates="disliked_by"
    )
    comments = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Video(db.Model):
    __tablename__ = "video"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # Automatically generate UUID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    description = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)

    views = Column(Integer, default=0)
    src = Column(JSON, nullable=False)
    properties = Column(JSON, nullable=False)
    thumbnail = Column(JSON, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="videos")
    liked_by = relationship(
        "User", secondary=user_liked_videos, back_populates="liked_videos"
    )
    disliked_by = relationship(
        "User", secondary=user_disliked_videos, back_populates="disliked_videos"
    )
    tags = relationship("Tag", secondary=video_tags, back_populates="videos")
    comments = relationship(
        "Comment", back_populates="video", cascade="all, delete-orphan"
    )


class Comment(db.Model):
    __tablename__ = "comment"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # Automatically generate UUID
    text = Column(String, nullable=False)

    video_id = Column(UUID(as_uuid=True), ForeignKey("video.id"))
    video = relationship("Video", back_populates="comments")

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="comments")
    created_at = Column(DateTime, default=datetime.utcnow)

class Tag(db.Model):
    __tablename__ = "tag"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # Automatically generate UUID
    title = Column(String(255), nullable=False)
    videos = relationship("Video", secondary=video_tags, back_populates="tags")


class Short(db.Model):
    __tablename__ = "short"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )  # Automatically generate UUID
    description = Column(String(255), nullable=False)
    thumbnail = Column(String, nullable=False)
    src = Column(JSON, nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="shorts")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
