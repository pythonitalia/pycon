import json

from authlib.integrations.starlette_client import OAuth
from starlette.responses import JSONResponse

from users.domain import services
from users.domain.services.social_login import SocialAccount, SocialLoginInput
from users.settings import (
    GOOGLE_AUTH_CLIENT_ID,
    GOOGLE_AUTH_CLIENT_SECRET,
    SOCIAL_LOGIN_JWT_COOKIE_NAME,
)

oauth = OAuth()


CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_id=str(GOOGLE_AUTH_CLIENT_ID),
    client_secret=str(GOOGLE_AUTH_CLIENT_SECRET),
    client_kwargs={"scope": "openid email profile"},
)


async def google_login(request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


async def google_login_auth(request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)

    if not user["email_verified"]:
        return JSONResponse({"error": "Email not verified"}, status_code=400)

    email = user["email"]
    user = await services.social_login(
        SocialLoginInput(
            email=email,
            social_account=SocialAccount(
                social_id=user["sub"],
                fullname=user["name"],
                first_name=user["given_name"],
                last_name=user["family_name"],
            ),
        ),
        users_repository=request.state.users_repository,
    )

    # response = RedirectResponse(url="/")
    # Temporary
    response = JSONResponse({"ok": True})
    response.set_cookie(
        SOCIAL_LOGIN_JWT_COOKIE_NAME, json.dumps({"jwt": user.generate_token()})
    )
    return response
