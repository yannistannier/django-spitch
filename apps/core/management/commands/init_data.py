from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from apps.authentication.models import User

from ._data import ADMINS

class Command(BaseCommand):
    help = 'Initializes the database with basic data'
    admins = ADMINS

    def handle(self, *args, **options):
        self.stdout.write('# init_data command start')
        self.add_admins()
        self.stdout.write('\n# init_data command end')

    def add_admins(self):
        self.stdout.write('\n>> Add admins')

        admins = getattr(self, 'admins', None)
        if admins:
            for admin in admins:
                email = admin.get('email')
                obj = User.objects.filter(email=email).first()
                if not obj:
                    obj = User.objects.create_superuser(**admin)
                    message = '"{}" has been created with id {}'.format(email, obj.pk)
                    self.stdout.write(self.style.SUCCESS(message))
                else:
                    message = '"{}" already exists with id {}'.format(email, obj.pk)
                    self.stdout.write(self.style.WARNING(message))
        else:
            self.stderr.write('No data to deal with')