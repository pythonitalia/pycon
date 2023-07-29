import json
from django.core.management.base import BaseCommand
from zipfile import ZipFile

from google_api.models import GoogleCloudOAuthCredential


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            help="Path to the file containing the credentials.",
        )

    def handle(self, file, *args, **options):
        zip_file = ZipFile(file)
        objs = []
        for info in zip_file.infolist():
            if not info.filename.endswith(".json") or info.filename.startswith(
                "__MACOSX"
            ):
                continue

            content = json.loads(zip_file.read(info.filename).decode("utf-8"))
            objs.append(
                GoogleCloudOAuthCredential(
                    client_id=content["installed"]["client_id"],
                    client_secret=content["installed"]["client_secret"],
                    project_id=content["installed"]["project_id"],
                    auth_uri=content["installed"]["auth_uri"],
                    token_uri=content["installed"]["token_uri"],
                    auth_provider_x509_cert_url=content["installed"][
                        "auth_provider_x509_cert_url"
                    ],
                )
            )

        GoogleCloudOAuthCredential.objects.bulk_create(objs)
