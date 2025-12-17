import uuid
from supabase import create_client
from django.conf import settings

supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_ROLE_KEY
)

def upload_to_supabase(file):
    filename = f"{uuid.uuid4()}_{file.name}"

    supabase.storage.from_("media").upload(
        filename,
        file.read(),
        {"content-type": file.content_type}
    )

    return f"{settings.MEDIA_URL}{filename}"