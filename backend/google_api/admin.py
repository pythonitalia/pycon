from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, reverse
from import_export.admin import ImportExportModelAdmin
from google_api.models import GoogleCloudOAuthCredential, GoogleCloudToken
import google_auth_oauthlib.flow
from django.utils.safestring import mark_safe
from django.core.cache import cache

from google_api.sdk import GOOGLE_CLOUD_SCOPES


class GoogleCloudTokenInline(admin.StackedInline):
    model = GoogleCloudToken


@admin.register(GoogleCloudOAuthCredential)
class GoogleCloudOAuthCredentialAdmin(ImportExportModelAdmin):
    inlines = [GoogleCloudTokenInline]

    def get_list_display(self, request):
        def authorize_client(obj):
            return self.authorize_client(obj, request)

        return ("project_id", authorize_client, "has_token")

    @admin.display(boolean=True)
    def has_token(self, obj):
        return obj.googlecloudtoken_set.exists()

    def authorize_client(self, obj, request):
        flow = self.build_google_flow(request, obj)
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type="offline",
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes="true",
        )
        cache.set(self.google_state_key(obj.id), state, 60 * 5)

        return mark_safe(f'<a href="{authorization_url}" target="_blank">Authorize</a>')

    def build_google_flow(self, request, obj, *, state=None):
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
            client_config={
                "installed": {
                    "client_id": obj.client_id,
                    "client_secret": obj.client_secret,
                    "project_id": obj.project_id,
                    "auth_uri": obj.auth_uri,
                    "token_uri": obj.token_uri,
                    "auth_provider_x509_cert_url": obj.auth_provider_x509_cert_url,
                }
            },
            scopes=GOOGLE_CLOUD_SCOPES,
            state=state,
        )
        flow.redirect_uri = request.build_absolute_uri(
            reverse("admin:auth-redirect", args=(obj.id,))
        )
        return flow

    def auth_redirect(self, request, object_id):
        stored_state = cache.get(self.google_state_key(object_id))
        param_state = request.GET.get("state")

        if stored_state != param_state:
            return

        obj = self.get_object(request, object_id)
        flow = self.build_google_flow(request, obj, state=param_state)
        flow.fetch_token(authorization_response=request.get_full_path())
        credentials = flow.credentials

        GoogleCloudToken.objects.filter(oauth_credential=obj).delete()

        GoogleCloudToken.objects.create(
            oauth_credential=obj,
            admin_user=request.user,
            token=credentials.token,
            refresh_token=credentials.refresh_token,
            token_uri=credentials.token_uri,
            client_id=credentials.client_id,
            client_secret=credentials.client_secret,
            scopes=credentials.scopes,
        )

        return redirect("admin:google_api_googlecloudoauthcredential_changelist")

    def google_state_key(self, object_id):
        return f"google_api:flow:{object_id}"

    def get_urls(self):
        return super().get_urls() + [
            path(
                "<int:object_id>/auth-redirect",
                self.admin_site.admin_view(self.auth_redirect),
                name="auth-redirect",
            )
        ]
