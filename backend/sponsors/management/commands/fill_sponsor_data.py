from django.core.management.base import BaseCommand
from django.db import transaction
from conferences.models import Conference
from sponsors.models import (
    SponsorLevel,
    SponsorBenefit,
    SponsorLevelBenefit,
    SponsorSpecialOption,
)


class Command(BaseCommand):
    help = "Create sponsor levels, benefits, and their relationships based on the provided table"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        conference = Conference.objects.last()

        SponsorLevelBenefit.objects.all().delete()
        SponsorBenefit.objects.all().delete()
        SponsorLevel.objects.all().delete()
        SponsorSpecialOption.objects.all().delete()

        # Create SponsorLevels
        levels = [
            {
                "name": "Keystone",
                "price": 10_000,
                "slots": 1,
                "highlight_color": "blue",
            },
            {
                "name": "Gold",
                "price": 7_000,
                "slots": 2,
                "highlight_color": "yellow",
            },
            {
                "name": "Silver",
                "price": 5_000,
                "slots": 5,
                "highlight_color": "gray",
            },
            {
                "name": "Bronze",
                "price": 3_000,
                "slots": 0,
                "highlight_color": "brown",
            },
            {
                "name": "Patron",
                "price": 2_000,
                "slots": 0,
                "highlight_color": "purple",
            },
            {
                "name": "Startup",
                "price": 500,
                "slots": 0,
                "highlight_color": "green",
            },
            {
                "name": "Diversity",
                "price": 1_000,
                "slots": 0,
                "highlight_color": "pink",
            },
        ]

        for level_data in levels:
            SponsorLevel.objects.create(
                conference=conference,
                name=level_data["name"],
                price=level_data["price"],
                slots=level_data["slots"],
                highlight_color=level_data["highlight_color"],
            )

        # Create SponsorBenefits with detailed descriptions
        benefits = [
            {
                "name": "Sponsored Keynote (1h)",
                "category": SponsorBenefit.Category.CONTENT,
                "description": "This sponsor will have the chance to give a keynote to the whole audience of the conference. The keynote content has to be arranged with the event organization and has to be something of interest and value for the community.",
            },
            {
                "name": "Sponsored talk (30min)",
                "category": SponsorBenefit.Category.CONTENT,
                "description": "These sponsors will have the chance to have a talk in the conference schedule. The talk content has to be arranged with the event organization and should have a technical relevance.",
            },
            {
                "name": "Booth in exhibit hall",
                "category": SponsorBenefit.Category.BOOTH,
                "description": "There will be a dedicated space for sponsors in the hotel hall where all the attendees will have coffee breaks and lunch. This package provides a 60x180cm table and comfortable chairs, with power supply and exclusive high-speed Wi-Fi access. Note: All additional booth customizations are the responsibility of the sponsor. Booth position selection will follow a first-come, first-served policy, and is determined by the sponsorship level.",
            },
            {
                "name": "Complimentary conference session passes",
                "category": SponsorBenefit.Category.PASSES,
                "description": "Free passes for the conference sessions.",
            },
            {
                "name": "Conference session passes with discount (30%)",
                "category": SponsorBenefit.Category.PASSES,
                "description": "Discounted passes for the conference sessions.",
            },
            {
                "name": "Social Event named after sponsor",
                "category": SponsorBenefit.Category.BRAND,
                "description": "The sponsors will see its name and logo shown during the social event and linked with that in all the related communication and official material.",
            },
            {
                "name": "Logo on video titles",
                "category": SponsorBenefit.Category.BRAND,
                "description": "These sponsors will have their logo shown in all the official videos recorded and published online of the event.",
            },
            {
                "name": "Logo on speaker desks",
                "category": SponsorBenefit.Category.BRAND,
                "description": "These sponsors will have their logo shown on the speakers podiums during all the conference talks.",
            },
            {
                "name": "Logo on banners",
                "category": SponsorBenefit.Category.BRAND,
                "description": "These sponsors will have their logo shown on the information banners placed in the congress center during the event.",
            },
            {
                "name": "Logo on website",
                "category": SponsorBenefit.Category.BRAND,
                "description": "These sponsors will have their logo shown on the official PyCon Italia website for the whole duration of the event.",
            },
            {
                "name": "Logo on digital signage",
                "category": SponsorBenefit.Category.BRAND,
                "description": "These sponsors will have their logo shown on digital signage throughout the event venue.",
            },
            {
                "name": "Recruiting track participation",
                "category": SponsorBenefit.Category.RECRUITING,
                "description": "The recruiting track will be hosted in a small and quiet room where the listed sponsors will have a time slot (highlighted in the schedule) in order to welcome all the interested people directly. Each sponsor will have a dedicated booking link where attendees can schedule their time slot.",
            },
            {
                "name": "Job positions in the Job Board on the website",
                "category": SponsorBenefit.Category.RECRUITING,
                "description": "PyCon Italia website has a job board advertising the job offers of our sponsors. This board will be online until the next PyCon is organized (usually October of the next year). This board will be promoted to the event attendees and Python Italia channels subscribers (~7.5k contacts).",
            },
            {
                "name": "One recruiting email to attendees (opt-in)",
                "category": SponsorBenefit.Category.RECRUITING,
                "description": "These sponsors will have the chance to send a dedicated email (through our systems, we don't give away any personal details) to the event attendees who will have opted-in to receive this kind of communications (usually about 1/4 of the total attendees).",
            },
            {
                "name": "Arranged newsletter content highlighting the sponsor",
                "category": SponsorBenefit.Category.CONTENT,
                "description": "This sponsor will have one special dedicated content in the official newsletter. The content will be arranged with the organization.",
            },
            {
                "name": "Questions in the conference feedback form",
                "category": SponsorBenefit.Category.ATTENDEE_INTERACTION,
                "description": "These sponsors will have the chance to suggest up to 2 questions in the feedback form sent to all the attendees after the event closing.",
            },
            {
                "name": "One tweet to all @PyConIT subscribers",
                "category": SponsorBenefit.Category.BRAND,
                "description": "These sponsors will have the chance to have one sponsored content tweeted directly on our Twitter account.",
            },
            {
                "name": "One post on all the official @PyConIT social channels",
                "category": SponsorBenefit.Category.BRAND,
                "description": 'These sponsors will have a "thank you" post on our social channels.',
            },
            {
                "name": "Participation in the gamification",
                "category": SponsorBenefit.Category.ATTENDEE_INTERACTION,
                "description": "Every year the PyCon Italia organization prepares a special game for the attendees. This sponsor have the chance to be included in this special initiative with a mention or more (details depends on the kind of game/riddle).",
            },
            {
                "name": "Shared meeting room",
                "category": SponsorBenefit.Category.BOOTH,
                "description": "These sponsors will have the chance to book a quiet meeting room just in front of the conference rooms. This room will have a shared calendar.",
            },
        ]

        for benefit_data in benefits:
            SponsorBenefit.objects.create(
                conference=conference,
                name=benefit_data["name"],
                category=benefit_data["category"],
                description=benefit_data["description"],
            )

        # Create SponsorLevelBenefits (same as before)
        level_benefits = {
            "Keystone": {
                "Sponsored Keynote (1h)": "✓",
                "Booth in exhibit hall": "✓",
                "Complimentary conference session passes": "6",
                "Conference session passes with discount (30%)": "10",
                "Social Event named after sponsor": "✓",
                "Logo on video titles": "✓",
                "Logo on speaker desks": "✓",
                "Logo on banners": "✓",
                "Logo on website": "✓",
                "Logo on digital signage": "✓",
                "Recruiting track participation": "✓",
                "Job positions in the Job Board on the website": "3",
                "One recruiting email to attendees (opt-in)": "✓",
                "Arranged newsletter content highlighting the sponsor": "✓",
                "Questions in the conference feedback form": "✓",
                "One tweet to all @PyConIT subscribers": "✓",
                "One post on all the official @PyConIT social channels": "✓",
                "Participation in the gamification": "✓",
                "Shared meeting room": "✓",
            },
            "Gold": {
                "Sponsored talk (30min)": "✓",
                "Booth in exhibit hall": "✓",
                "Complimentary conference session passes": "4",
                "Conference session passes with discount (30%)": "8",
                "Logo on video titles": "✓",
                "Logo on speaker desks": "✓",
                "Logo on banners": "✓",
                "Logo on website": "✓",
                "Logo on digital signage": "✓",
                "Recruiting track participation": "✓",
                "Job positions in the Job Board on the website": "2",
                "One recruiting email to attendees (opt-in)": "✓",
                "Questions in the conference feedback form": "✓",
                "One tweet to all @PyConIT subscribers": "✓",
                "One post on all the official @PyConIT social channels": "✓",
                "Shared meeting room": "✓",
            },
            # Add other levels (Silver, Bronze, Patron, Startup, Diversity) here...
        }

        for level_name, benefits in level_benefits.items():
            level = SponsorLevel.objects.get(name=level_name, conference=conference)
            for benefit_name, value in benefits.items():
                benefit = SponsorBenefit.objects.get(
                    name=benefit_name, conference=conference
                )
                SponsorLevelBenefit.objects.create(
                    sponsor_level=level,
                    benefit=benefit,
                    value=value,
                )

        special_options = [
            {
                "name": "Advertising in the PyCon Italia Digital Signage",
                "description": "Your advertisement will be shown on the program/information displays in the venue during the conference. (additional ADs cost is €500 each) ADs may be still images or short videos, the content must be provided by the sponsor company and will be shown on the conference location during all the conference time.",
                "price": 1000.00,
            },
            {
                "name": "Sponsored Selfie / Pic Background",
                "description": "The sponsor will have its logo shown on the big selfie / pic background (4.1mt * 2mt), that will be put just near to the registration/information desk for the whole event.",
                "price": 2000.00,
            },
            {
                "name": "Beginners' Workshop Sponsor",
                "description": "The sponsor will have its name and logo shown along all the communication and during this initiative (~120 people).",
                "price": 1000.00,
            },
            {
                "name": "Network Area Sponsor (Logo and Name of the Network Area)",
                "description": "The sponsor will have its name and logo shown on the communication and in this area where people can stay, relax, chat and network together.",
                "price": 2000.00,
            },
            {
                "name": "Logo on Lanyard (Lanyard Included)",
                "description": "The sponsor will have its logo printed on all the lanyards of the attendees.",
                "price": 1500.00,
            },
            {
                "name": "Workshop Sponsor (Logo in Training Rooms)",
                "description": "The sponsor logo will be shown in the training room for the whole event duration.",
                "price": 1500.00,
            },
            {
                "name": "Optional Booth in Front of Conference Rooms",
                "description": "The sponsor can have an extra desk in front of the conference rooms - this option may not be available for safety reasons.",
                "price": 2000.00,
            },
            {
                "name": "Optional Small Table in Front of Conference Rooms",
                "description": "The sponsor can have an extra small round (80cm diameter) high table in front of the conference rooms - this option may not be available for safety reasons.",
                "price": 800.00,
            },
            {
                "name": "More Job Positions in the Job Board",
                "description": "The sponsor can have more slots available to be published in the Job Board.",
                "price": 200.00,
            },
        ]

        for option_data in special_options:
            SponsorSpecialOption.objects.create(
                conference=conference,
                name=option_data["name"],
                description=option_data["description"],
                price=option_data["price"],
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully created sponsor levels, benefits, their relationships, and special options"
            )
        )
