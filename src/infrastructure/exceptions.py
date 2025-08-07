class DBError(Exception):
    def __init__(self, message="DB error") -> None:
        super().__init__()


class S3Error(Exception):
    def __init__(self, original_exception: Exception) -> None:
        self.original_exception = original_exception
        super().__init__(str(original_exception))
