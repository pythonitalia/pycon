import datetime
import sqlite3
from datetime import timedelta

import pytz
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError

from languages.models import Language
from pycon.settings.base import root


DEFAULT_DB_PATH = root('p3.db')
SUPPORTED_ENTITIES = ['user', 'conference']
OLD_DEAFAULT_TZ = pytz.timezone('Europe/Rome')

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def string_to_tzdatetime(s, day_end=False):
    if not s:
        return None
    unaware_date = datetime.datetime.fromisoformat(s)
    if day_end:
        unaware_date += timedelta(days=1, seconds=-1)
    return pytz.utc.localize(unaware_date)


def create_languages():
    en, _ = Language.objects.get_or_create(code='en', defaults={'name': 'English'})
    it, _ = Language.objects.get_or_create(code='it', defaults={'name': 'Italiano'})
    return [en, it]


class Command(BaseCommand):
    help = 'Import old Pycon Site database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--db',
            dest='db_path',
            action='store',
            help='Absolute path of the SQLite db file',
        )
        parser.add_argument(
            '--entities',
            dest='entities',
            action='store',
            help='List of comma separated entities to import, i.e. user,conference',
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

    def import_conferences(self):
        from conferences.models import Conference, Deadline

        self.stdout.write(f'Importing conferences...')

        languages = create_languages()

        old_conf = list(self.c.execute('SELECT * FROM conference_conference'))

        created = 0
        for old_conf in old_conf:
            try:
                with transaction.atomic():
                    conf = Conference.objects.create(
                        name=old_conf['name'],
                        code=old_conf['code'],
                        timezone=OLD_DEAFAULT_TZ,
                        # topics=None,  # TODO
                        # audience_levels=None,  # TODO
                        # submission_types=None,  # TODO
                        start=string_to_tzdatetime(old_conf['conference_start']),
                        end=string_to_tzdatetime(old_conf['conference_end'], day_end=True),
                    )

                    conf.languages.set(languages)

                    for deadline in ['cfp', 'voting', 'refund']:
                        Deadline.objects.create(
                            conference=conf,
                            name=deadline,
                            type=deadline,
                            start=string_to_tzdatetime(old_conf[f'{deadline}_start']),
                            end=string_to_tzdatetime(old_conf[f'{deadline}_end'], day_end=True),
                        )
            except IntegrityError as exc:
                self.stdout.write(self.style.NOTICE(f"Cannot import conference {old_conf['name']} (maybe it's already there): {exc}"))
                continue
            except Exception as exc:
                self.stdout.write(self.style.NOTICE(f'Something bad happened when importing conference {old_conf["name"]}: {exc}'))
                continue
            else:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'{created} conferences imported.'))

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

        entities = SUPPORTED_ENTITIES
        if options['entities']:
            entities = options['entities'].split(',')

        if 'user' in entities:
            self.import_users()
        if 'conference' in entities:
            self.import_conferences()

        self.stdout.write(self.style.SUCCESS('Done!'))
