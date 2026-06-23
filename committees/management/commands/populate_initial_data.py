from django.core.management.base import BaseCommand
from committees.models import Committee

class Command(BaseCommand):
    help = 'Populates the database with the 9 initial committees from the README'

    def handle(self, *args, **kwargs):
        committees_list = [
            'Catering Committee',
            'Music Committee',
            'Organizing Committee',
            'Finance Committee',
            'DRAPO Committee',
            'Communication Committee',
            'Testify Committee',
            'Flowering Committee',
            'Secretarial Committee',
        ]

        for name in committees_list:
            Committee.objects.get_or_create(name=name)
            self.stdout.write(self.style.SUCCESS(f'Successfully created {name}'))