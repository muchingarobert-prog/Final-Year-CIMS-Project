from django.core.management.base import BaseCommand

from committees.models import Committee


class Command(BaseCommand):

    help = "Populate church committees"

    def handle(self, *args, **kwargs):

        committees = [
            "DRAPO",
            "MUSIC",
            "TESTIFY",
            "COMMUNICATIONS",
            "FLOWERING",
            "SECRETARIAT",
            "ORGANIZING",
            "FIRST AID",
            "CATERING",
            "FINANCE",
        ]

        for committee_name in committees:

            Committee.objects.get_or_create(
                name=committee_name
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Committees created successfully."
            )
        )