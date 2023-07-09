from .base import AppExceptionCase
from fastapi import status


class AudioSampleIncorrectContentType(AppExceptionCase):
    def __init__(self, context: dict = None):
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        super().__init__(status_code, context)


class AudioSampleCreateFailed(AppExceptionCase):
    def __init__(self, context: dict = None):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(status_code, context)


class AudioSampleNotFound(AppExceptionCase):
    def __init__(self, context: dict = None):
        status_code = status.HTTP_404_NOT_FOUND
        super().__init__(status_code, context)


class AudioSampleApprovalStatusUpdateFailed(AppExceptionCase):
    def __init__(self, context: dict = None):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(status_code, context)


class AudioSampleDeleteFailed(AppExceptionCase):
    def __init__(self, context: dict = None):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        super().__init__(status_code, context)


# class LabelCreateFailed(AppExceptionCase):
#     def __init__(self, context: dict = None):
#         """
#         Label Creation Failed
#         """
#         status_code = 500
#         super().__init__(status_code, context)


# class LabelUpdateFailed(AppExceptionCase):
#     def __init__(self, context: dict = None):
#         status_code = 500
#         super().__init__(status_code, context)


# class LabelDeleteFailed(AppExceptionCase):
#     def __init__(self, context: dict = None):
#         status_code = 500
#         super().__init__(status_code, context)


# class LabelNotFound(AppExceptionCase):
#     def __init__(self, context: dict = None):
#         status_code = 404
#         super().__init__(status_code, context)


# class LabelAlreadyExists(AppExceptionCase):
#     def __init__(self, context: dict = None):
#         status_code = 400
#         super().__init__(status_code, context)
