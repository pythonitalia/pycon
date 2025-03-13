import strawberry


@strawberry.type
class BillingAddress:
    id: strawberry.ID
    is_business: bool
    company_name: str
    user_given_name: str
    user_family_name: str
    zip_code: str
    city: str
    address: str
    country: str
    vat_id: str
    fiscal_code: str
    sdi: str
    pec: str

    @classmethod
    def from_django_model(cls, instance):
        return cls(
            id=instance.id,
            is_business=instance.is_business,
            company_name=instance.company_name,
            user_given_name=instance.user_given_name,
            user_family_name=instance.user_family_name,
            zip_code=instance.zip_code,
            city=instance.city,
            address=instance.address,
            country=instance.country,
            vat_id=instance.vat_id,
            fiscal_code=instance.fiscal_code,
            sdi=instance.sdi,
            pec=instance.pec,
        )
