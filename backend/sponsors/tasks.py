from django.urls import reverse

from notifications.models import EmailTemplate, EmailTemplateIdentifier
from pycon.celery import app
from pycon.signing import sign_path
from sponsors.models import SponsorLead
from integrations import slack


@app.task
def send_sponsor_brochure(sponsor_lead_id):
    sponsor_lead = SponsorLead.objects.get(id=sponsor_lead_id)
    conference = sponsor_lead.conference

    view_brochure_path = reverse("view-brochure", args=[sponsor_lead_id])
    signed_path = sign_path(view_brochure_path)

    brochure_link = f"https://admin.pycon.it{signed_path}"

    email_template = EmailTemplate.objects.for_conference(conference).get_by_identifier(
        EmailTemplateIdentifier.sponsorship_brochure
    )
    email_template.send_email(
        recipient_email=sponsor_lead.email,
        placeholders={
            "brochure_link": brochure_link,
            "conference_name": conference.name.localize("en"),
        },
    )


@app.task
def notify_new_sponsor_lead_via_slack(*, sponsor_lead_id, admin_absolute_uri):
    sponsor_lead = SponsorLead.objects.get(id=sponsor_lead_id)
    conference = sponsor_lead.conference
    company = sponsor_lead.company

    message = f"New Sponsor Lead: {company}"
    admin_path = reverse("admin:sponsors_sponsorlead_change", args=[sponsor_lead_id])
    slack.send_message(
        [
            {
                "type": "section",
                "text": {
                    "text": message,
                    "type": "plain_text",
                },
                "fields": [
                    {"type": "mrkdwn", "text": "*Consent to email*"},
                    {"type": "plain_text", "text": " "},
                    {
                        "type": "mrkdwn",
                        "text": "Yes"
                        if sponsor_lead.consent_to_contact_via_email
                        else "No",
                    },
                ],
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
        text=message,
        oauth_token=conference.get_slack_oauth_token(),
        channel_id=conference.slack_new_sponsor_lead_channel_id,
    )
