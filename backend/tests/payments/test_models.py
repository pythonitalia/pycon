from payments.models import Payment


def test_str():
    x = Payment(
        total=100,
        currency='EUR'
    )

    assert str(x) == f'EUR 100 on {x.created:%B %d, %Y %H:%m}'
