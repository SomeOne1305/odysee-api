import uuid

def is_valid_uuid(uuid_to_test):
        """Проверяет, является ли строка корректным UUID."""
        try:
            uuid.UUID(str(uuid_to_test))
            return True
        except ValueError:
            return False