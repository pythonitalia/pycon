from strawberry_forms.mutations import FormMutation

from .forms import LoginForm, RegisterForm
from .types import MeUser


class Login(FormMutation):
    @classmethod
    def transform(cls, result):
        return MeUser(
            id=result.id,
            email=result.email,
            first_name=result.first_name,
            last_name=result.last_name,
            gender=result.gender,
            date_birth=result.date_birth,
            business_name=result.business_name,
            fiscal_code=result.fiscal_code,
            vat_number=result.vat_number,
            recipient_code=result.recipient_code,
            pec_address=result.pec_address,
            address=result.address,
            phone_number=result.phone_number,
        )

    class Meta:
        form_class = LoginForm
        output_types = (MeUser,)


class Register(FormMutation):
    @classmethod
    def transform(cls, result):
        return MeUser(
            id=result.id,
            email=result.email,
            first_name=result.first_name,
            last_name=result.last_name,
            gender=result.gender,
            date_birth=result.date_birth,
            business_name=result.business_name,
            fiscal_code=result.fiscal_code,
            vat_number=result.vat_number,
            recipient_code=result.recipient_code,
            pec_address=result.pec_address,
            address=result.address,
            phone_number=result.phone_number,
        )

    class Meta:
        form_class = RegisterForm
        output_types = (MeUser,)


class UsersMutations:
    login = Login.Mutation
    register = Register.Mutation
