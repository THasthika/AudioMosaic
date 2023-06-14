from .base import AppExceptionCase


class DatasetCreateFailed(AppExceptionCase):
    def __init__(self, context: dict = None):
        """
        Dataset Creation Failed
        """
        status_code = 500
        super().__init__(status_code, context)


class DatasetUpdateFailed(AppExceptionCase):
    def __init__(self, context: dict = None):
        status_code = 500
        super().__init__(status_code, context)


class DatasetDeleteFailed(AppExceptionCase):
    def __init__(self, context: dict = None):
        status_code = 500
        super().__init__(status_code, context)


class DatasetNotFound(AppExceptionCase):
    def __init__(self, context: dict = None):
        status_code = 404
        super().__init__(status_code, context)
