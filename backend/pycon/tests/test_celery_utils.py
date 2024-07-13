import os
import hashlib
from pycon.celery_utils import make_lock_id


def test_func():
    pass


def test_make_lock_id(mocker):
    mocker.patch.dict(os.environ, {"PYTEST_XDIST_WORKER": ""})
    key = make_lock_id(test_func)
    assert key == "celery_lock_pycon.tests.test_celery_utils_test_func"

    key = make_lock_id(test_func, 1, 2, 3)
    args_md5 = hashlib.md5("123".encode("utf-8")).hexdigest()
    assert key == f"celery_lock_pycon.tests.test_celery_utils_test_func_{args_md5}"

    mocker.patch.dict(os.environ, {"PYTEST_XDIST_WORKER": "1"})
    key = make_lock_id(test_func)
    assert key == "celery_lock_pycon.tests.test_celery_utils_test_func_1"
