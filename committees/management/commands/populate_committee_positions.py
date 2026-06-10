from django.core.management.base import BaseCommand

from committees.models import CommitteePosition


class Command(BaseCommand):

    help = "Populate committee positions"

    def handle(self, *args, **kwargs):

        positions = [
            "Chairperson",
            "Vice Chairperson",
            "Secretary",
            "Vice Secretary",
            "Treasurer",
            "Vice Treasurer",
            "Committee Member",
        ]

        for position in positions:

            CommitteePosition.objects.get_or_create(
                title=position
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Committee positions created successfully."
            )
        )