import os
import hashlib
import threading
import time
from pycon.celery_utils import make_lock_id, renew_lock


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


def test_renew_lock(mocker):
    stop_event = threading.Event()
    lock = mocker.Mock()
    lock.owned.return_value = True

    renew_thread = threading.Thread(target=renew_lock, args=(lock, 0.1, stop_event))
    renew_thread.daemon = True
    renew_thread.start()

    time.sleep(0.3)

    assert lock.extend.call_count > 0

    stop_event.set()
    renew_thread.join()


def test_renew_lock_stops_if_lock_is_not_owned(mocker):
    stop_event = threading.Event()
    lock = mocker.Mock()
    lock.owned.return_value = False

    renew_thread = threading.Thread(target=renew_lock, args=(lock, 0.1, stop_event))
    renew_thread.daemon = True
    renew_thread.start()

    time.sleep(0.3)

    assert lock.extend.call_count == 0

    stop_event.set()
    renew_thread.join()


def test_renew_lock_stops_if_lock_renew_failed(mocker):
    stop_event = threading.Event()
    lock = mocker.Mock()
    lock.owned.return_value = True
    lock.extend.side_effect = ValueError("Error")

    renew_thread = threading.Thread(target=renew_lock, args=(lock, 0.1, stop_event))
    renew_thread.daemon = True
    renew_thread.start()

    time.sleep(0.3)

    assert lock.extend.call_count == 1

    renew_thread.join()
