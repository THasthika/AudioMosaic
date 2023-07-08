import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_sqlalchemy_orm():
    def _mock_sqlalchemy_orm(
        configs: list[tuple[list[str], tuple[str, any]]] | list[str],
        last_func: tuple[str, any] = None,
    ):
        db = MagicMock()

        if last_func is not None:
            configs = [(configs, last_func)]

        for config in configs:
            (funcs, last_func) = config
            for x in funcs:
                db.__getattr__(x).return_value = db
            db.__getattr__(last_func[0]).return_value = last_func[1]
        return db

    return _mock_sqlalchemy_orm


@pytest.fixture
def mock_repository():
    def _mock_repository(
        *, exceptions: list[tuple[str, Exception, list[any]]] = []
    ):
        repo = MagicMock()

        for func_name, excep, args in exceptions:

            def _temp(*_args):
                raise excep(*args)

            repo.__getattr__(func_name).side_effect = _temp

        return repo

    return _mock_repository


# # @pytest.fixture
# # def mock_sqlalchemy_session(mocker):
# #     mock = mocker.patch(
# #         "sqlalchemy.orm.Session").return_value = mocker.Mock()
# #     return mock
