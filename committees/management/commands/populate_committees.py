from django.core.management.base import BaseCommand

from committees.models import Committee


class Command(BaseCommand):

    help = "Populate church committees"

    def handle(self, *args, **kwargs):

        committees = [
            "DRAPO",
            "Music",
            "Testify",
            "Communications and Media",
            "Flowering",
            "Secretariat",
            "Organizing",
            "First Aid",
            "Catering",
            "Finance",
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