from django.urls import reverse
from django.core.signing import Signer

from pycon.celery import app
from sponsors.models import SponsorLead
from notifications.emails import send_email
from integrations import slack


@app.task
def send_sponsor_brochure(sponsor_lead_id):
    sponsor_lead = SponsorLead.objects.get(id=sponsor_lead_id)
    subject_prefix = f"[{sponsor_lead.conference.name.localize('en')}]"

    signer = Signer()
    view_brochure_path = reverse("view-brochure", args=[sponsor_lead_id])
    signed_url = signer.sign(view_brochure_path)
    signature = signed_url.split(":")[-1]

    brochure_link = f"https://admin.pycon.it{view_brochure_path}?sh={signature}"

    send_email(
        template="sponsorship-brochure",
        to=sponsor_lead.email,
        subject=f"{subject_prefix} Our Sponsorship Brochure",
        variables={"brochurelink": brochure_link},
        reply_to=[
            "sponsor@pycon.it",
        ],
    )


@app.task
def notify_new_sponsor_lead_via_slack(*, sponsor_lead_id, admin_absolute_uri):
    sponsor_lead = SponsorLead.objects.get(id=sponsor_lead_id)
    conference = sponsor_lead.conference
    company = sponsor_lead.company
    admin_path = reverse("admin:sponsors_sponsorlead_change", args=[sponsor_lead_id])
    slack.send_message(
        [
            {
                "type": "section",
                "text": {
                    "text": f"New Sponsor lead from {company}",
                    "type": "plain_text",
                },
            }
        ],
        [
            {
                "blocks": [
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Open in Admin",
                                    "emoji": True,
                                },
                                "action_id": "ignore-action",
                                "url": f"{admin_absolute_uri}{admin_path[1:]}",
                            }
                        ],
                    }
                ]
            }
        ],
        token=conference.slack_new_sponsor_lead_incoming_webhook_url,
    )
