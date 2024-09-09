class ReadImageError(Exception):
    def __init__(self, path: str):
        message = f"Failed to read image {path}, are you sure it exists?"
        super(ReadImageError, self).__init__(message)
