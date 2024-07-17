def test_importing_settings(mocker):
    # test that importing settings does not raise any exception
    mocker.patch("pycon.settings.base.env")
    mocker.patch("boto3.client")

    from pycon.settings import prod  # noqa
    from pycon.settings import dev  # noqa
    from pycon.settings import test  # noqa
    from pycon.settings import base  # noqa


def test_enable_logfire(mocker):
    mock_logfire = mocker.patch("pycon.settings.base.logfire")

    from pycon.settings.dev import enable_logfire  # noqa

    enable_logfire("test")

    mock_logfire.configure.assert_called_once_with(token="test")
