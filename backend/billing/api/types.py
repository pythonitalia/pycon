import strawberry
import strawberry_django

from billing import models


@strawberry_django.type(models.BillingAddress)
class BillingAddress:
    id: strawberry.auto
    is_business: strawberry.auto
    company_name: strawberry.auto
    user_given_name: strawberry.auto
    user_family_name: strawberry.auto
    zip_code: strawberry.auto
    city: strawberry.auto
    address: strawberry.auto
    country: strawberry.auto
    vat_id: strawberry.auto
    fiscal_code: strawberry.auto
    sdi: strawberry.auto
    pec: strawberry.auto
