import datetime
import sqlite3
from datetime import timedelta
from decimal import Decimal

import pytz
from django.contrib.contenttypes.models import ContentType
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError

from conferences.models import AudienceLevel, Topic, Duration, Conference, TicketFare
from languages.models import Language
from orders.enums import PaymentState
from orders.models import Order, OrderItem
from pycon.settings.base import root
from schedule.models import Room
from submissions.models import SubmissionType, Submission
from tickets.models import Ticket
from users.models import User

DEFAULT_DB_PATH = root('p3.db')
OLD_DEAFAULT_TZ = pytz.timezone('Europe/Rome')
TALK_TYPES = {
    's': 'Talk',
    'i': 'Interactive',
    't': 'Training',
    'p': 'Poster session',
    'h': 'Help desk',
}
TOPIC_MAPPING = {
    # (track.title,       sub_community): topic
    ('DjangoVillage',     '*'):          'DjangoVillage',
    ('PyWebTwo',          'django'):     'DjangoVillage',
    ('Python&Friends',    'django'):     'DjangoVillage',
    ('PyWeb&Friends',     'django'):     'DjangoVillage',
    ('PyWeb',             'django'):     'DjangoVillage',
    ('PyWeb',             '*'):          'PyWeb',
    ('PyWebTwo',          '*'):          'PyWeb',
    ('PyWeb&Friends',     '*'):          'PyWeb&Friends',
    ('PyWeb / DevOps',    '*'):          'PyWeb / DevOps',
    ('PyBusiness',        '*'):          'PyBusiness',
    ('PyTraining',        'pybusiness'): 'PyBusiness',
    ('Python&Friends',    'pybusiness'): 'PyBusiness',
    ('PyLang',            '*'):          'PyLang',
    ('PyData',            '*'):          'PyData',
    ('PyDataTwo',         '*'):          'PyData',
    ('PyDataTwo',         '*'):          'PyData',
    ('PyDataTrainingTwo', '*'):          'PyData',
    ('PyDataTrainingTwo', '*'):          'PyData',
    ('PyDataTrainingOne', '*'):          'PyData',
    ('PyDataTrainingOne', '*'):          'PyData',
    ('PyDataTraining',    '*'):          'PyData',
    ('PyDatabase',        '*'):          'PyDatabase',
    ('PyData&Friends',    '*'):          'PyData&Friends',
    ('PyCommunity',       '*'):          'PyCommunity',
    ('Odoo',              '*'):          'Odoo',
    ('PyBusiness',        'odoo'):       'Odoo',
    ('*',                 'pydata'):     'PyData',
    ('*',                 '*'):          'Python & Friends',
}


def get_topic_name(track_title, sub_community):
    topic_name = TOPIC_MAPPING.get((track_title, sub_community))
    if topic_name:
        return topic_name

    topic_name = TOPIC_MAPPING.get((track_title, '*'))
    if topic_name:
        return topic_name

    topic_name = TOPIC_MAPPING.get(('*', sub_community))
    if topic_name:
        return topic_name

    return TOPIC_MAPPING.get(('*', '*'))


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
        created_count = skipped_count = 0
        for submission_type in TALK_TYPES.values():
            _, created = SubmissionType.objects.get_or_create(name=submission_type)
            if created:
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Submission Types: {created_count} created, {skipped_count} skipped.'
        ))

    def create_topics(self, overwrite=False):
        if overwrite:
            self.stdout.write(f'Overwrite has no effect on topics')
        created_count = skipped_count = 0
        for topic in list(self.c.execute('SELECT title FROM conference_track')):
            _, created = Topic.objects.get_or_create(name=topic['title'])
            if created:
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Topics: {created_count} created, {skipped_count} skipped.'
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

                    topic_list = list(self.c.execute(
                        'select distinct t.title '
                        'from conference_track t, conference_schedule s '
                        'where s.id = t.schedule_id and s.conference=?',
                        [conf.code]
                    ))
                    conf.topics.set(
                        Topic.objects.filter(name__in=[t['title'] for t in topic_list])
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

    def import_submissions(self, overwrite=False):
        if overwrite:
            self.stdout.write(f'Overwrite is the default for submissions')

        self.stdout.write(f'Importing submissions...')

        conferences = {
            conf.code: conf.id
            for conf in Conference.objects.all()
        }
        languages = {
            lang.code: lang.id
            for lang in Language.objects.all()
        }
        submission_types = {
            st.name: st.id
            for st in SubmissionType.objects.all()
        }
        types = {
            code: submission_types[name]
            for code, name in TALK_TYPES.items()
        }

        talk_list = list(self.c.execute(
            """
            select talk.conference, talk.duration, talk.type, talk.created, talk.title, talk.language, talk.type, 
                content.body, user.username,
                track.title as track_title, talk2.sub_community
            from conference_talk talk
            left outer join conference_multilingualcontent content 
                on content.object_id = talk.id and content.content_type_id = 25 and content.content = 'abstracts'
            left outer join conference_talkspeaker speaker 
                on speaker.talk_id = talk.id 
            left outer join auth_user user 
                on user.id = speaker.speaker_id             
            left outer join conference_event event 
                on event.talk_id = talk.id
            left outer join conference_schedule sched 
                on sched.conference = talk.conference and sched.id = event.schedule_id
            left outer join conference_eventtrack et 
                on et.event_id = event.id
            left outer join conference_track track 
                on track.schedule_id = sched.id and track.id = et.track_id
            left outer join p3_p3talk talk2 
                on talk2.talk_id = talk.id
            """
        ))

        actions = {'create': 0, 'update': 0, 'skip': 0, 'error': 0}
        for talk in talk_list:
            action = 'create'
            try:
                with transaction.atomic():
                    duration, _ = Duration.objects.get_or_create(
                        conference_id=conferences[talk['conference']],
                        duration=talk['duration'],
                        defaults=dict(
                            name=f"{talk['duration']} minutes"
                        )
                    )
                    duration.allowed_submission_types.add(types[talk['type']])

                    topic_name = get_topic_name(talk['track_title'], talk['sub_community'])
                    topic, _ = Topic.objects.get_or_create(name=topic_name)

                    conf, created = Submission.objects.update_or_create(
                        created=string_to_tzdatetime(talk['created']),
                        conference_id=conferences[talk['conference']],
                        title=talk['title'],
                        language_id=languages.get(talk['language']),
                        defaults=dict(
                            speaker=User.objects.get(username=talk['username']),
                            abstract=talk['body'],
                            topic=topic,
                            type_id=types[talk['type']],
                            duration=duration,
                        )
                    )
                    if not created:
                        action = 'update'

            except IntegrityError as exc:
                action = 'skip'
                continue
            except Exception as exc:
                self.stdout.write(self.style.NOTICE(
                    f'Something bad happened when importing submission {talk["title"]}: {exc}'
                ))
                action = 'error'
                continue
            finally:
                actions[action] += 1

        self.stdout.write(self.style.SUCCESS(
            f'Submission: '
            f'{actions["create"]} created, '
            f'{actions["update"]} updated, '
            f'{actions["skip"]} skipped, '
            f'{actions["error"]} errors.'
        ))

    def import_tickets(self, overwrite):
        if overwrite:
            self.stdout.write(f'Overwrite is the default for tickets')

        self.stdout.write(f'Importing tickets...')

        conferences = {
            conf.code: conf.id
            for conf in Conference.objects.all()
        }
        users_by_email = {
            user.email: user.id
            for user in User.objects.all()
        }

        ticket_list = list(self.c.execute(
            """
            SELECT
                ticket2.assigned_to as ticket_user,
                user.email as order_user,
                fare.conference, fare.code as fare_code, fare.description as fare_description, fare.name as fare_name,
                fare.price,
                ord.method as payment_method, ord.payment_url, ord._complete as payment_complete,
                ord.created as order_created,
                orderitem.description as orderitem_description, orderitem.price as orderitem_price
            from conference_ticket ticket
            join p3_ticketconference ticket2 on ticket2.ticket_id = ticket.id
            left outer join auth_user user on user.id = ticket.user_id
            left outer join conference_fare fare on fare.id = ticket.fare_id
            left outer join assopy_orderitem orderitem on orderitem.ticket_id = ticket.id
            left outer join assopy_order ord on orderitem.order_id = ord.id
            """
        ))

        actions = {'create': 0, 'update': 0, 'skip': 0, 'error': 0}
        for orig_ticket in ticket_list:
            action = 'create'
            try:
                with transaction.atomic():

                    order_user = users_by_email[orig_ticket['order_user']]
                    ticket_user = users_by_email.get(orig_ticket['ticket_user'], order_user)

                    ticket_fare, _ = TicketFare.objects.update_or_create(
                        conference_id=conferences[orig_ticket['conference']],
                        code=orig_ticket['fare_code'],
                        defaults=dict(
                            name=orig_ticket['fare_name'],
                            description=orig_ticket['fare_description'],
                            price=Decimal(orig_ticket['price']),
                        )
                    )

                    order, _ = Order.objects.update_or_create(
                        created=string_to_tzdatetime(orig_ticket['order_created']),
                        user_id=order_user,
                        defaults=dict(
                            provider=orig_ticket['payment_method'],
                            transaction_id=orig_ticket['payment_url'],
                            state=PaymentState.COMPLETE if orig_ticket['payment_complete'] == 1 else PaymentState.FAILED,
                            amount=1,
                        )
                    )

                    orderitem, _ = OrderItem.objects.update_or_create(
                        order=order,
                        item_type=ContentType.objects.get_for_model(OrderItem),
                        item_object_id=ticket_fare.id,
                        description=orig_ticket['orderitem_description'],
                        unit_price=Decimal(orig_ticket['orderitem_price']),
                        defaults=dict(
                            created=order.created,
                            quantity=1,
                        )
                    )

                    ticket, created = Ticket.objects.update_or_create(
                        user_id=ticket_user,
                        ticket_fare=ticket_fare,
                        order=order,
                        defaults=dict(
                            created=order.created,
                        )
                    )
                    if not created:
                        action = 'update'
                    print(f'{action}d ticket {ticket.id}')

            except IntegrityError as exc:
                action = 'skip'
                continue
            except Exception as exc:
                self.stdout.write(self.style.NOTICE(
                    f'Something bad happened when importing ticket {orig_ticket["id"]}: {exc}'
                ))
                action = 'error'
                continue
            finally:
                actions[action] += 1

        # recalculate amounts and quantities for orders and orderitems
        for orderitem in OrderItem.objects.select_for_update().all():
            orderitem.quantity = Ticket.objects.filter(
                order=orderitem.order, ticket_fare_id=orderitem.item_object_id
            ).count()
            orderitem.save()
        for order in Order.objects.all():
            order.amount = sum(order.items.all().extra(
                select={'item_amount': 'quantity * unit_price'}
            ).values_list('item_amount', flat=True))
            order.save()

        self.stdout.write(self.style.SUCCESS(
            f'Tickets: '
            f'{actions["create"]} created, '
            f'{actions["update"]} updated, '
            f'{actions["skip"]} skipped, '
            f'{actions["error"]} errors.'
        ))

    def import_rooms(self, overwrite=False):
        if overwrite:
            self.stdout.write(f'Overwrite has no effect on rooms')

        self.stdout.write(f'Importing rooms...')

        conferences = {
            conf.code: conf.id
            for conf in Conference.objects.all()
        }

        track_list = list(self.c.execute(
            """
            select schedule.conference, track.title
            from conference_track track
            left outer join conference_schedule schedule on schedule.id = track.schedule_id
            """
        ))

        actions = {'create': 0, 'update': 0, 'skip': 0, 'error': 0}
        for track in track_list:
            action = 'create'
            try:
                with transaction.atomic():
                    room, created = Room.objects.get_or_create(
                        name=track['title'],
                        conference_id=conferences[track['conference']],
                    )
                    if not created:
                        action = 'skip'
            except Exception as exc:
                self.stdout.write(self.style.NOTICE(
                    f'Something bad happened when importing track/room {track["title"]}: {exc}'
                ))
                action = 'error'
                continue
            finally:
                actions[action] += 1

        self.stdout.write(self.style.SUCCESS(
            f'Rooms: '
            f'{actions["create"]} created, '
            f'{actions["update"]} updated, '
            f'{actions["skip"]} skipped, '
            f'{actions["error"]} errors.'
        ))

    def db_connect(self, options):
        db_path = options['db_path']
        if not db_path:
            self.stdout.write(self.style.NOTICE('DB path not specified, using default.'))
            db_path = DEFAULT_DB_PATH
        self.stdout.write(f'Using DB: {db_path}')

        conn = sqlite3.connect(db_path)
        conn.row_factory = dict_factory
        self.c = conn.cursor()

    def handle(self, *args, **options):
        self.stdout.write('Starting...')

        self.db_connect(options)

        entities = 'all'
        overwrite = False
        if options['entities']:
            entities = options['entities'].split(',')
            overwrite = options['overwrite']
        elif options['overwrite']:
            raise CommandError('Cannot overwrite without --entities parameter')

        if overwrite:
            self.stdout.write(self.style.NOTICE('This command will overwrite entities in the destination DB!!!'))

        if 'user' in entities or entities == 'all':
            self.import_users(overwrite=overwrite)
        if 'submission_type' in entities or entities == 'all':
            self.create_submission_types(overwrite=overwrite)
        if 'topic' in entities or entities == 'all':
            self.create_topics(overwrite=overwrite)
        if 'conference' in entities or entities == 'all':
            self.import_conferences(overwrite=overwrite)
        if 'room' in entities or entities == 'all':
            self.import_rooms(overwrite=overwrite)
        if 'submission' in entities or entities == 'all':
            self.import_submissions(overwrite=overwrite)
        if 'ticket' in entities or entities == 'all':
            self.import_tickets(overwrite=overwrite)

        self.stdout.write(self.style.SUCCESS('Done!'))
