import sqlite3

from django.core.management.base import BaseCommand

from pycon.settings.base import root


DEFAULT_DB_PATH = root('p3.db')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Command(BaseCommand):
    help = 'Import old Pycon Site database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--db',
            dest='db_path',
            action='store',
            help='Absolute path of the SQLite db file',
        )

    def import_users(self):
        from users.models import User

        self.stdout.write(f'Importing users...')

        old_users = list(self.c.execute('SELECT * FROM auth_user'))
        old_usernames = {u['username'] for u in old_users}
        new_usernames = {u.username for u in User.objects.all()}
        skipping_users = new_usernames.intersection(old_usernames)
        if skipping_users:
            self.stdout.write(self.style.NOTICE(f'Skipping {len(skipping_users)} because they already exist'))
        result = User.objects.bulk_create([
            User(
                username=user['username'],
                email=user['email'],
                password=user['password'],
                is_active=user['is_active'],
                date_joined=user['date_joined'],
                is_staff=user['is_staff'],
                is_superuser=user['is_superuser'],
            ) for user in old_users if user['username'] not in new_usernames
        ])

        self.stdout.write(self.style.SUCCESS(f'{len(result)} users imported.'))

    def handle(self, *args, **options):
        self.stdout.write('Starting...')

        db_path = options['db_path']
        if not db_path:
            self.stdout.write(self.style.NOTICE('DB path not specified, using default.'))
            db_path = DEFAULT_DB_PATH
        self.stdout.write(f'Using DB: {db_path}')

        conn = sqlite3.connect(db_path)
        conn.row_factory = dict_factory
        self.c = conn.cursor()

        self.import_users()

        self.stdout.write(self.style.SUCCESS('Done!'))
