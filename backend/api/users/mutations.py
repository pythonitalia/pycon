from strawberry_forms.mutations import FormMutation
from submissions.permissions import IsAuthenticated

from .forms import LoginForm, RegisterForm, UpdateForm, UpdateImageForm
from .types import Image, MeUser


def get_me_user_type(result):
    return MeUser(
        id=result.id,
        email=result.email,
        first_name=result.first_name,
        last_name=result.last_name,
        gender=result.gender,
        open_to_recruiting=result.open_to_recruiting,
        open_to_newsletter=result.open_to_newsletter,
        date_birth=result.date_birth,
        business_name=result.business_name,
        fiscal_code=result.fiscal_code,
        vat_number=result.vat_number,
        recipient_code=result.recipient_code,
        pec_address=result.pec_address,
        address=result.address,
        country=result.country,
        phone_number=result.phone_number,
    )


class BaseUserMutation(FormMutation):
    @classmethod
    def transform(cls, result):
        return MeUser(
            id=result.id,
            image=Image(url=result.image),
            email=result.email,
            first_name=result.first_name,
            last_name=result.last_name,
            gender=result.gender,
            open_to_recruiting=result.open_to_recruiting,
            open_to_newsletter=result.open_to_newsletter,
            date_birth=result.date_birth,
            business_name=result.business_name,
            fiscal_code=result.fiscal_code,
            vat_number=result.vat_number,
            recipient_code=result.recipient_code,
            pec_address=result.pec_address,
            address=result.address,
            country=result.country,
            phone_number=result.phone_number,
        )

    class Meta:

        form_class = RegisterForm
        output_types = (MeUser,)


class Login(BaseUserMutation):
    class Meta:
        form_class = LoginForm
        output_types = (MeUser,)


class Register(BaseUserMutation):
    class Meta:
        form_class = RegisterForm
        output_types = (MeUser,)


class Update(BaseUserMutation):
    class Meta:
        form_class = UpdateForm
        output_types = (MeUser,)
        permission_classes = (IsAuthenticated,)


class UpdateImage(BaseUserMutation):
    class Meta:
        form_class = UpdateImageForm
        output_types = (MeUser,)
        permission_classes = (IsAuthenticated,)


class UsersMutations:
    login = Login.Mutation
    register = Register.Mutation
    update = Update.Mutation
    update_image = UpdateImage.Mutation
