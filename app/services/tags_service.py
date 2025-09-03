from ..extensions import db
from ..models import Tag


class TagsService:
    @staticmethod
    def create_tag(title: str):
        """
        Creates a new tag in the database.
        """
        tag = Tag(title=title)
        db.session.add(tag)
        db.session.commit()
        return tag
    @staticmethod
    def tag_exists(title: str) -> bool:
        """
        Checks if a tag with the given title already exists in the database.
        """
        return db.session.query(Tag.query.filter_by(title=title).exists()).scalar()
    
    @staticmethod
    def get_all():
        """
        Retrieve all tags from the database.
        Returns a list of tag dictionaries.
        """
        tags = Tag.query.all()
        return [{"id": tag.id, "title": tag.title} for tag in tags]
    
    @staticmethod
    def get_tag_by_id(tag_id: str):
        """
        Retrieve a tag by its ID.
        """
        return Tag.query.get(tag_id)

    
    @staticmethod
    def update_tag(tag_id: str, title: str):
        """
        Updates a tag's title in the database.
        """
        tag = Tag.query.get(tag_id)
        if tag:
            tag.title = title
            db.session.commit()

    @staticmethod
    def delete_tag(tag_id:str):
        """Delete specific tag with ID"""
        tag = Tag.query.get(tag_id)
        if tag:
            db.session.delete(tag)
            db.session.commit()