from uuid import UUID


def is_valid_uuid(string_value, version=4):
    try:
        uuid = UUID(str(string_value), version=version)
        return uuid
    except ValueError:
        return None

