from decimal import Decimal

from django.core.management.base import BaseCommand
from grants.models import Grant, GrantReimbursement, GrantReimbursementCategory
from conferences.models import Conference


class Command(BaseCommand):
    help = "Backfill GrantReimbursement entries from approved_type data on approved grants."

    def handle(self, *args, **options):
        self.stdout.write("🚀 Starting backfill of grant reimbursements...")

        self._ensure_categories_exist()
        self._migrate_grants()
        self._validate_migration()

        self.stdout.write(self.style.SUCCESS("✅ Backfill completed successfully."))

    def _ensure_categories_exist(self):
        for conference in Conference.objects.all():
            GrantReimbursementCategory.objects.get_or_create(
                conference=conference,
                category="ticket",
                defaults={
                    "name": "Ticket",
                    "description": "Conference ticket",
                    "max_amount": conference.grants_default_ticket_amount
                    or Decimal("0.00"),
                    "included_by_default": True,
                },
            )
            GrantReimbursementCategory.objects.get_or_create(
                conference=conference,
                category="travel",
                defaults={
                    "name": "Travel",
                    "description": "Travel support",
                    "max_amount": conference.grants_default_travel_from_extra_eu_amount
                    or Decimal("400.00"),
                    "included_by_default": False,
                },
            )
            GrantReimbursementCategory.objects.get_or_create(
                conference=conference,
                category="accommodation",
                defaults={
                    "name": "Accommodation",
                    "description": "Accommodation support",
                    "max_amount": conference.grants_default_accommodation_amount
                    or Decimal("300.00"),
                    "included_by_default": True,
                },
            )

    def _migrate_grants(self):
        grants = Grant.objects.filter(approved_type__isnull=False).exclude(
            approved_type=""
        )

        self.stdout.write(f"📦 Migrating {grants.count()} grants...")

        for grant in grants:
            categories = {
                c.category: c
                for c in GrantReimbursementCategory.objects.filter(
                    conference=grant.conference
                )
            }

            def add_reimbursement(category_key, amount):
                if category_key in categories and amount:
                    GrantReimbursement.objects.get_or_create(
                        grant=grant,
                        category=categories[category_key],
                        defaults={
                            "granted_amount": amount,
                        },
                    )

            add_reimbursement("ticket", grant.ticket_amount)

            if grant.approved_type in ("ticket_travel", "ticket_travel_accommodation"):
                add_reimbursement("travel", grant.travel_amount)

            if grant.approved_type in (
                "ticket_accommodation",
                "ticket_travel_accommodation",
            ):
                add_reimbursement("accommodation", grant.accommodation_amount)

    def _validate_migration(self):
        errors = []
        grants = Grant.objects.filter(approved_type__isnull=False).exclude(
            approved_type=""
        )

        for grant in grants:
            original_total = sum(
                filter(
                    None,
                    [
                        grant.ticket_amount,
                        grant.travel_amount,
                        grant.accommodation_amount,
                    ],
                )
            )
            reimbursements_total = sum(
                r.granted_amount for r in GrantReimbursement.objects.filter(grant=grant)
            )

            if abs(original_total - reimbursements_total) > Decimal("0.01"):
                errors.append(
                    f"Grant ID {grant.id} total mismatch: expected {original_total}, got {reimbursements_total}"
                )

        if errors:
            self.stdout.write(
                self.style.ERROR(f"⚠️ Found {len(errors)} grants with mismatched totals")
            )
            for msg in errors:
                self.stdout.write(self.style.WARNING(f"  {msg}"))
        else:
            self.stdout.write(
                self.style.SUCCESS("🧮 All grant totals match correctly.")
            )
