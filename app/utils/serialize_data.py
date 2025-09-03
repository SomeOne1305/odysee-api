from sqlalchemy.inspection import inspect


def serialize_data(instance):
    if not hasattr(instance, "__table__"):
        raise TypeError("Expected a SQLAlchemy model instance.")

    # Initialize the serialized data dictionary
    serialized_data = {}

    # Serialize regular columns
    for column in inspect(instance).mapper.column_attrs:
        serialized_data[column.key] = getattr(instance, column.key)

    # Serialize relationships
    for relationship in inspect(instance).mapper.relationships:
        related_value = getattr(instance, relationship.key)
        if related_value is not None:
            if relationship.uselist:
                # Many-to-many or one-to-many relationship
                serialized_data[relationship.key] = [
                    serialize_data(rel) for rel in related_value
                ]
            else:
                # One-to-one or many-to-one relationship
                serialized_data[relationship.key] = serialize_data(related_value)

    return serialized_data
