from strawberry.tools import create_type

from api.blob.mutations import generate_participant_avatar_upload_url

BlobMutation = create_type("BlobMutation", [generate_participant_avatar_upload_url])
