from django.http import HttpResponse
from visa.models import InvitationLetterRequest, InvitationLetterRequestStatus
from pycon.signing import require_signed_request
from django.shortcuts import redirect


@require_signed_request
def download_invitation_letter(request, id: int):
    invitation_letter_request = InvitationLetterRequest.objects.filter(id=id).first()

    if (
        not invitation_letter_request
        or invitation_letter_request.status != InvitationLetterRequestStatus.SENT
    ):
        return HttpResponse(
            "We can't find this invitation letter request. Please contact us.",
            status=404,
        )

    return redirect(invitation_letter_request.invitation_letter.url, permanent=False)
