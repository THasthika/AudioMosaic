from .base import AppExceptionCase


class LabelCreateFailed(AppExceptionCase):
    def __init__(self, context: dict = None):
        """
        Label Creation Failed
        """
        status_code = 500
        super().__init__(status_code, context)


class LabelUpdateFailed(AppExceptionCase):
    def __init__(self, context: dict = None):
        status_code = 500
        super().__init__(status_code, context)


class LabelDeleteFailed(AppExceptionCase):
    def __init__(self, context: dict = None):
        status_code = 500
        super().__init__(status_code, context)


class LabelNotFound(AppExceptionCase):
    def __init__(self, context: dict = None):
        status_code = 404
        super().__init__(status_code, context)


class LabelAlreadyExists(AppExceptionCase):
    def __init__(self, context: dict = None):
        status_code = 400
        super().__init__(status_code, context)
