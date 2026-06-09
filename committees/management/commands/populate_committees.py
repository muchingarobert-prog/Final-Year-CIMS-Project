from django.core.management.base import BaseCommand
from committees.models import Committee


class Command(BaseCommand):

    help = "Populate church committees"

    def handle(self, *args, **kwargs):

        committees = [
            (
                'CATERING',
                'Handles food and catering services'
            ),
            (
                'MUSIC',
                'Music and orchestra management'
            ),
            (
                'ORGANIZING',
                'Planning and organizing events'
            ),
            (
                'FINANCE',
                'Budget and fund management'
            ),
            (
                'DRAPO',
                'Drama and poetry activities'
            ),
            (
                'COMMUNICATION',
                'Audio and communication systems'
            ),
            (
                'TESTIFY',
                'Doctrinal and faith matters'
            ),
            (
                'FLOWERING',
                'Church beautification'
            ),
            (
                'SECRETARIAL',
                'Records and documentation'
            ),
        ]

        for name, description in committees:

            Committee.objects.get_or_create(
                name=name,
                defaults={
                    'description': description
                }
            )

        self.stdout.write(
            self.style.SUCCESS(
                'Committees created successfully.'
            )
        )