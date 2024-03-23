def test_importing_settings(mocker):
    # test that importing settings does not raise any exception
    mocker.patch("pycon.settings.base.env")

    from pycon.settings import prod  # noqa
    from pycon.settings import dev  # noqa
    from pycon.settings import test  # noqa
    from pycon.settings import base  # noqa
