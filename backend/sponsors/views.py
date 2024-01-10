from django.core.signing import Signer, BadSignature
from django.http import HttpResponseForbidden
from sponsors.models import SponsorLead

from wagtail.documents import get_document_model
from django.shortcuts import redirect


def view_brochure(request, sponsor_lead_id):
    signer = Signer()
    signature = request.GET.get("sh", None)
    try:
        signer.unsign(f"{request.path}:{signature}")
    except BadSignature:
        return HttpResponseForbidden("Invalid signature.")

    sponsor_lead = SponsorLead.objects.get(id=sponsor_lead_id)
    sponsor_lead.brochure_viewed = True
    sponsor_lead.save(update_fields=["brochure_viewed"])

    Document = get_document_model()
    brochure = Document.objects.filter(
        tags__name__in=["sponsorship-brochure", sponsor_lead.conference.code],
    ).first()

    return redirect(brochure.url, permanent=False)
