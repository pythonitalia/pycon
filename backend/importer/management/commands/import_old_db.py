import datetime
import sqlite3
from datetime import timedelta

import pytz
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError

from conferences.models import AudienceLevel
from languages.models import Language
from pycon.settings.base import root
from submissions.models import SubmissionType

DEFAULT_DB_PATH = root('p3.db')
SUPPORTED_ENTITIES = ['user', 'conference']
OLD_DEAFAULT_TZ = pytz.timezone('Europe/Rome')
TALK_TYPES = {
    's': 'Talk',
    'i': 'Interactive',
    't': 'Training',
    'p': 'Poster session',
    'h': 'Help desk',
}

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


def create_audience_levels():
    beginner, _ = AudienceLevel.objects.get_or_create(name='Beginner')
    intermediate, _ = AudienceLevel.objects.get_or_create(name='Intermediate')
    advanced, _ = AudienceLevel.objects.get_or_create(name='Advanced')
    return [beginner, intermediate, advanced]


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
        parser.add_argument(
            '--overwrite',
            dest='overwrite',
            action='store_true',
            help='Overwrite entities if found (needs --entities parameter)',
        )

    def import_users(self, overwrite=False):
        if overwrite:
            self.stdout.write(self.style.ERROR(f'Users import does not support overwriting.'))

        from users.models import User

        self.stdout.write(f'Importing users...')

        old_users = list(self.c.execute('SELECT * FROM auth_user'))
        old_usernames = {u['username'] for u in old_users}
        new_usernames = {u.username for u in User.objects.all()}
        existent_users = new_usernames.intersection(old_usernames)
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

        self.stdout.write(self.style.SUCCESS(
            f'Users: {len(result)} created, {len(existent_users)} skipped.'
        ))

    def create_submission_types(self, overwrite=False):
        if overwrite:
            self.stdout.write(f'Overwrite has no effect on submission type')
        created_count = updated_count = 0
        for submission_type in TALK_TYPES.values():
            _, created = SubmissionType.objects.get_or_create(name=submission_type)
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Submission Types: {created_count} created, {updated_count} updated.'
        ))

    def import_conferences(self, overwrite=False):
        from conferences.models import Conference, Deadline

        self.stdout.write(f'Importing conferences...')

        languages = create_languages()
        audience_levels = create_audience_levels()

        old_conf_list = list(self.c.execute('SELECT * FROM conference_conference'))

        actions = {'create': 0, 'update': 0, 'skip': 0, 'error': 0}
        for old_conf in old_conf_list:
            action = 'create'
            try:
                with transaction.atomic():
                    key_fields = dict(code=old_conf['code'])
                    fields = dict(
                        name=old_conf['name'],
                        timezone=OLD_DEAFAULT_TZ,
                        # topics=None,  # TODO
                        start=string_to_tzdatetime(old_conf['conference_start']),
                        end=string_to_tzdatetime(old_conf['conference_end'], day_end=True),
                    )
                    if overwrite:
                        conf, created = Conference.objects.update_or_create(**key_fields, defaults=fields)
                        action = 'create' if created else 'update'
                    else:
                        conf = Conference.objects.create(**key_fields, **fields)
                        action = 'create'

                    conf.languages.set(languages)
                    conf.audience_levels.set(audience_levels)

                    submission_types = list(self.c.execute(
                        'select distinct type from conference_talk where conference=?', [conf.code]
                    ))
                    conf.submission_types.set(
                        SubmissionType.objects.filter(name__in=[
                            TALK_TYPES[st['type']] for st in submission_types
                        ])
                    )

                    for deadline in ['cfp', 'voting', 'refund']:
                        Deadline.objects.create(
                            conference=conf,
                            name=deadline,
                            type=deadline,
                            start=string_to_tzdatetime(old_conf[f'{deadline}_start']),
                            end=string_to_tzdatetime(old_conf[f'{deadline}_end'], day_end=True),
                        )
            except IntegrityError as exc:
                self.stdout.write(f"Cannot import conference {old_conf['name']} (maybe it's already there): {exc}")
                action = 'skip'
                continue
            except Exception as exc:
                self.stdout.write(self.style.NOTICE(
                    f'Something bad happened when importing conference {old_conf_list["name"]}: {exc}'
                ))
                action = 'error'
                continue
            finally:
                actions[action] += 1

        self.stdout.write(self.style.SUCCESS(
            f'Conferences: '
            f'{actions["create"]} created, '
            f'{actions["update"]} updated, '
            f'{actions["skip"]} skipped, '
            f'{actions["error"]} errors.'
        ))

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
        overwrite = False
        if options['entities']:
            entities = options['entities'].split(',')
            overwrite = options['overwrite']
        elif options['overwrite']:
            raise CommandError('Cannot overwrite without --entities parameter')

        if overwrite:
            self.stdout.write(self.style.NOTICE('This command will overwrite entities in the destination DB!!!'))

        if 'user' in entities:
            self.import_users(overwrite=overwrite)
        if 'submission_type' in entities:
            self.create_submission_types(overwrite=overwrite)
        if 'conference' in entities:
            self.import_conferences(overwrite=overwrite)

        self.stdout.write(self.style.SUCCESS('Done!'))
