import datetime
import json
import sqlite3
from datetime import timedelta

import pytz
from conferences.models import AudienceLevel, Conference, Duration, Topic
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from languages.models import Language
from pycon.settings.base import root
from schedule.models import Room, ScheduleItem
from submissions.models import Submission, SubmissionType
from users.models import User

DEFAULT_DB_PATH = root("p3.db")
OLD_DEAFAULT_TZ = pytz.timezone("Europe/Rome")
TALK_TYPES = {
    "s": "Talk",
    "i": "Interactive",
    "t": "Training",
    "p": "Poster session",
    "h": "Help desk",
}
TOPIC_MAPPING = {
    # (track.title,       sub_community): topic
    ("DjangoVillage", "*"): "DjangoVillage",
    ("PyWebTwo", "django"): "DjangoVillage",
    ("Python&Friends", "django"): "DjangoVillage",
    ("PyWeb&Friends", "django"): "DjangoVillage",
    ("PyWeb", "django"): "DjangoVillage",
    ("PyWeb", "*"): "PyWeb",
    ("PyWebTwo", "*"): "PyWeb",
    ("PyWeb&Friends", "*"): "PyWeb&Friends",
    ("PyWeb / DevOps", "*"): "PyWeb / DevOps",
    ("PyBusiness", "*"): "PyBusiness",
    ("PyTraining", "pybusiness"): "PyBusiness",
    ("Python&Friends", "pybusiness"): "PyBusiness",
    ("PyLang", "*"): "PyLang",
    ("PyData", "*"): "PyData",
    ("PyDataTwo", "*"): "PyData",
    ("PyDataTwo", "*"): "PyData",
    ("PyDataTrainingTwo", "*"): "PyData",
    ("PyDataTrainingTwo", "*"): "PyData",
    ("PyDataTrainingOne", "*"): "PyData",
    ("PyDataTrainingOne", "*"): "PyData",
    ("PyDataTraining", "*"): "PyData",
    ("PyDatabase", "*"): "PyDatabase",
    ("PyData&Friends", "*"): "PyData&Friends",
    ("PyCommunity", "*"): "PyCommunity",
    ("Odoo", "*"): "Odoo",
    ("PyBusiness", "odoo"): "Odoo",
    ("*", "pydata"): "PyData",
    ("*", "*"): "Python & Friends",
}


def i18n_json(value, languages=None):
    if not languages:
        languages = Language.objects.all()
    field = {l.code: value for l in languages}
    return json.dumps(field)


def get_topic_name(track_title, sub_community):
    topic_name = TOPIC_MAPPING.get((track_title, sub_community))
    if topic_name:
        return topic_name

    topic_name = TOPIC_MAPPING.get((track_title, "*"))
    if topic_name:
        return topic_name

    topic_name = TOPIC_MAPPING.get(("*", sub_community))
    if topic_name:
        return topic_name

    return TOPIC_MAPPING.get(("*", "*"))


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def string_to_tzdatetime(s, day_end=False, timezone=None):
    if not s:
        return None
    unaware_date = datetime.datetime.fromisoformat(s)
    if day_end:
        unaware_date += timedelta(days=1, seconds=-1)
    if timezone:
        return unaware_date.replace(tzinfo=timezone)
    else:
        return pytz.utc.localize(unaware_date)


def create_languages():
    en, _ = Language.objects.get_or_create(code="en", defaults={"name": "English"})
    it, _ = Language.objects.get_or_create(code="it", defaults={"name": "Italiano"})
    return [en, it]


def create_audience_levels():
    beginner, _ = AudienceLevel.objects.get_or_create(name="Beginner")
    intermediate, _ = AudienceLevel.objects.get_or_create(name="Intermediate")
    advanced, _ = AudienceLevel.objects.get_or_create(name="Advanced")
    return [beginner, intermediate, advanced]


class Command(BaseCommand):
    help = "Import old Pycon Site database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--db",
            dest="db_path",
            action="store",
            help="Absolute path of the SQLite db file",
        )
        parser.add_argument(
            "--entities",
            dest="entities",
            action="store",
            help="List of comma separated entities to import, i.e. user,conference",
        )
        parser.add_argument(
            "--overwrite",
            dest="overwrite",
            action="store_true",
            help="Overwrite entities if found (needs --entities parameter)",
        )

    def import_users(self, overwrite=False):
        if overwrite:
            self.stdout.write(
                self.style.ERROR(f"Users import does not support overwriting.")
            )

        from users.models import User

        self.stdout.write(f"Importing users...")

        old_users = list(
            self.c.execute(
                """
            select
                user.id,
                user.username,
                user.first_name as name,
                user.first_name || " " || user.last_name as full_name,
                user.email,
                user.password,
                user.is_active,
                user.is_staff,
                user.is_superuser,
                user.date_joined,
                IFNULL(useridentity.gender, "") as gender,
                IFNULL(ca.birthday, useridentity.birthday) AS date_birth,
                assopy_user.country_id as country,
                IFNULL(p3p3p.spam_recruiting, 0) as open_to_recruiting
            from auth_user user
            left join assopy_user
                on assopy_user.user_id = user.id
            left join assopy_useridentity useridentity
                on user.email = useridentity.email
            left join conference_attendeeprofile ca
                on assopy_user.user_id = ca.user_id
            left join conference_presence cp
                on ca.user_id = cp.profile_id
            left join p3_p3profile p3p3p
                on cp.profile_id = p3p3p.profile_id
            group by user.email
            order by user.id
        """
            )
        )

        # TODO: this might break other imports if they are based on the PK
        # we don't need bulk create or update as this script is only ran once
        created = 0
        updated = 0

        for user in old_users:
            print(f"Importing {user['email']}")
            _, created = User.objects.update_or_create(
                email=user["email"],
                defaults={
                    "password": user["password"],
                    "is_active": user["is_active"],
                    "is_staff": user["is_staff"],
                    "is_superuser": user["is_superuser"],
                    "name": user["name"],
                    "full_name": user["full_name"],
                    "date_birth": user["date_birth"],
                    "open_to_recruiting": user["open_to_recruiting"],
                },
            )

            if created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Users: {created} created, {updated} "
                f"updated, of {len(old_users)} found in the old db."
            )
        )

    def create_submission_types(self, overwrite=False):
        if overwrite:
            self.stdout.write(f"Overwrite has no effect on submission type")
        created_count = skipped_count = 0
        for submission_type in TALK_TYPES.values():
            _, created = SubmissionType.objects.get_or_create(name=submission_type)
            if created:
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Submission Types: {created_count} created, {skipped_count} skipped."
            )
        )

    def create_topics(self, overwrite=False):
        if overwrite:
            self.stdout.write(f"Overwrite has no effect on topics")
        created_count = skipped_count = 0
        for topic in list(self.c.execute("SELECT title FROM conference_track")):
            _, created = Topic.objects.get_or_create(name=topic["title"])
            if created:
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Topics: {created_count} created, {skipped_count} skipped."
            )
        )

    def import_conferences(self, overwrite=False):
        from conferences.models import Conference, Deadline

        self.stdout.write(f"Importing conferences...")

        languages = create_languages()
        audience_levels = create_audience_levels()

        old_conf_list = list(self.c.execute("SELECT * FROM conference_conference"))

        actions = {"create": 0, "update": 0, "skip": 0, "error": 0}
        for old_conf in old_conf_list:
            action = "create"
            try:
                with transaction.atomic():
                    key_fields = dict(code=old_conf["code"])

                    fields = dict(
                        name=i18n_json(
                            old_conf["name"].replace(" ", ""), languages=languages
                        ),
                        timezone=OLD_DEAFAULT_TZ,
                        start=string_to_tzdatetime(old_conf["conference_start"]),
                        end=string_to_tzdatetime(
                            old_conf["conference_end"], day_end=True
                        ),
                        introduction=i18n_json(
                            old_conf["name"].replace(" ", ""), languages=languages
                        ),
                    )
                    if overwrite:
                        conf, created = Conference.objects.update_or_create(
                            **key_fields, defaults=fields
                        )
                        action = "create" if created else "update"
                    else:
                        conf = Conference.objects.get_or_create(**key_fields, **fields)[
                            0
                        ]
                        action = "create"

                    conf.languages.set(languages)
                    conf.audience_levels.set(audience_levels)

                    submission_types = list(
                        self.c.execute(
                            """
                            select distinct type
                            from conference_talk
                            where conference=?
                            """,
                            [conf.code],
                        )
                    )
                    conf.submission_types.set(
                        SubmissionType.objects.filter(
                            name__in=[TALK_TYPES[st["type"]] for st in submission_types]
                        )
                    )

                    topic_list = list(
                        self.c.execute(
                            "select distinct t.title "
                            "from conference_track t, conference_schedule s "
                            "where s.id = t.schedule_id and s.conference=?",
                            [conf.code],
                        )
                    )
                    conf.topics.set(
                        Topic.objects.filter(name__in=[t["title"] for t in topic_list])
                    )

                    for deadline in ["cfp", "voting", "refund"]:
                        Deadline.objects.create(
                            conference=conf,
                            name=i18n_json(deadline, languages=languages),
                            type=deadline,
                            start=string_to_tzdatetime(old_conf[f"{deadline}_start"]),
                            end=string_to_tzdatetime(
                                old_conf[f"{deadline}_end"], day_end=True
                            ),
                        )
            except IntegrityError:
                action = "skip"
                continue
            except Exception as exc:
                msg = (
                    f"Something bad happened when importing conference "
                    f'{old_conf_list["name"]}: {exc}'
                )
                self.stdout.write(self.style.NOTICE(msg))
                action = "error"
                continue
            finally:
                actions[action] += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Conferences: "
                f'{actions["create"]} created, '
                f'{actions["update"]} updated, '
                f'{actions["skip"]} skipped, '
                f'{actions["error"]} errors.'
            )
        )

    def import_submissions(self, overwrite=False):
        if overwrite:
            self.stdout.write(f"Overwrite is the default for submissions")

        self.stdout.write(f"Importing submissions...")

        conferences = {conf.code: conf.id for conf in Conference.objects.all()}
        languages = {lang.code: lang.id for lang in Language.objects.all()}
        submission_types = {st.name: st.id for st in SubmissionType.objects.all()}
        types = {code: submission_types[name] for code, name in TALK_TYPES.items()}
        users_by_email = {user.email: user.id for user in User.objects.all()}

        talk_list = list(
            self.c.execute(
                """
            select
                talk.id, talk.conference, talk.duration, talk.type,
                talk.created, talk.title, talk.language, talk.type,
                content.body,
                track.title as track_title, talk2.sub_community,
                (select user.email from conference_talkspeaker speaker
                left outer join auth_user user on user.id = speaker.speaker_id
                where speaker.talk_id = talk.id and speaker.helper = 0
                order by speaker.id limit 1) as speaker_email
            from conference_talk talk
            left outer join conference_multilingualcontent content
                on content.object_id = talk.id
                and content.content_type_id = 25
                and content.content = 'abstracts'
            left outer join conference_event event
                on event.talk_id = talk.id
            left outer join conference_schedule sched
                on sched.conference = talk.conference
                and sched.id = event.schedule_id
            left outer join conference_eventtrack et
                on et.event_id = event.id
            left outer join conference_track track
                on track.schedule_id = sched.id and track.id = et.track_id
            left outer join p3_p3talk talk2
                on talk2.talk_id = talk.id
            """
            )
        )

        actions = {"create": 0, "update": 0, "skip": 0, "error": 0}
        for talk in talk_list:
            action = "create"
            try:
                with transaction.atomic():
                    duration, _ = Duration.objects.get_or_create(
                        conference_id=conferences[talk["conference"]],
                        duration=talk["duration"],
                        defaults=dict(name=f"{talk['duration']} minutes"),
                    )
                    duration.allowed_submission_types.add(types[talk["type"]])

                    topic_name = get_topic_name(
                        talk["track_title"], talk["sub_community"]
                    )
                    topic, _ = Topic.objects.get_or_create(name=topic_name)

                    submission, created = Submission.objects.update_or_create(
                        created=string_to_tzdatetime(talk["created"]),
                        conference_id=conferences[talk["conference"]],
                        title=talk["title"],
                        language_id=languages.get(talk["language"]),
                        defaults=dict(
                            speaker_id=users_by_email.get(talk["speaker_email"]),
                            abstract=talk["body"],
                            topic=topic,
                            type_id=types[talk["type"]],
                            duration=duration,
                        ),
                    )
                    if not created:
                        action = "update"

            except IntegrityError:
                action = "skip"
                continue
            except Exception as exc:
                msg = (
                    f"Something bad happened when importing submission"
                    f' {talk["title"]}: {exc}'
                )
                self.stdout.write(self.style.NOTICE(msg))
                action = "error"
                continue
            finally:
                actions[action] += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Submission: "
                f'{actions["create"]} created, '
                f'{actions["update"]} updated, '
                f'{actions["skip"]} skipped, '
                f'{actions["error"]} errors.'
            )
        )

    def import_schedule_items(self, overwrite=False):
        if overwrite:
            self.stdout.write(f"Overwrite is the default for schedule items")

        self.stdout.write(f"Importing schedule items...")

        conferences = {conf.code: conf.id for conf in Conference.objects.all()}
        rooms = {room.name: room.id for room in Room.objects.all()}
        submissions = {
            (s.created, s.conference_id, s.title, s.language.code): s
            for s in Submission.objects.all()
        }
        users_by_email = {user.email: user.id for user in User.objects.all()}

        si_list = list(
            self.c.execute(
                """
            select distinct
                sched.conference, sched.date,
                event.id as event_id, event.custom as event_custom,
                event.abstract as event_abstract,
                event.start_time, event.duration,
                talk.id as talk_id, talk.created as talk_created,
                talk.title as talk_title,
                talk.language as talk_language
            from conference_schedule sched
            left outer join conference_event event
                on sched.id = event.schedule_id
            left outer join conference_talk talk
                on event.talk_id = talk.id
            order by sched.slug
            """
            )
        )

        actions = {"create": 0, "update": 0, "skip": 0, "error": 0}
        for si in si_list:
            action = "create"
            try:
                with transaction.atomic():
                    conference_id = conferences.get(si["conference"])
                    submission = None

                    if si["talk_id"]:
                        submission_key = (
                            string_to_tzdatetime(si["talk_created"]),
                            conference_id,
                            si["talk_title"],
                            si["talk_language"],
                        )
                        submission = submissions.get(submission_key)

                    start_datetime = string_to_tzdatetime(
                        f"{si['date']} {si['start_time']}", timezone=OLD_DEAFAULT_TZ
                    )
                    end_datetime = start_datetime + timedelta(minutes=si["duration"])

                    sched_item, _ = ScheduleItem.objects.update_or_create(
                        conference_id=conference_id,
                        title=si["event_custom"] or si["talk_title"],
                        description=si["event_abstract"],
                        type="submission" if submission else "custom",
                        submission=submission,
                        start=start_datetime,
                        end=end_datetime,
                    )

                    if submission:
                        speakers_emails = list(
                            self.c.execute(
                                """
                            select user.email
                            from conference_talkspeaker speaker
                            left outer join auth_user user
                                on user.id = speaker.speaker_id
                            where speaker.talk_id = ?
                            and user.email <> ?
                            """,
                                [si["talk_id"], submission.speaker.email],
                            )
                        )
                        for se in speakers_emails:
                            sched_item.additional_speakers.add(
                                users_by_email[se["email"]]
                            )

                    room_list = list(
                        self.c.execute(
                            """
                        select track.title
                        from conference_event event
                        join conference_eventtrack et on et.event_id = event.id
                        join conference_track track on track.id = et.track_id
                        where event.id = ?
                        """,
                            [si["event_id"]],
                        )
                    )
                    for room in room_list:
                        sched_item.rooms.add(rooms[room["title"]])

            except IntegrityError:
                action = "skip"
                continue
            except Exception as exc:
                msg = (
                    f"Something bad happened when importing submission for "
                    f'event_id={si["event_id"]}: {exc}'
                )
                self.stdout.write(self.style.NOTICE(msg))
                action = "error"
                continue
            finally:
                actions[action] += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Schedule Items: "
                f'{actions["create"]} created, '
                f'{actions["update"]} updated, '
                f'{actions["skip"]} skipped, '
                f'{actions["error"]} errors.'
            )
        )

    def import_rooms(self, overwrite=False):
        if overwrite:
            self.stdout.write(f"Overwrite has no effect on rooms")

        self.stdout.write(f"Importing rooms...")

        conferences = {conf.code: conf.id for conf in Conference.objects.all()}

        track_list = list(
            self.c.execute(
                """
            select schedule.conference, track.title
            from conference_track track
            left outer join conference_schedule schedule
                on schedule.id = track.schedule_id
            """
            )
        )

        actions = {"create": 0, "update": 0, "skip": 0, "error": 0}
        for track in track_list:
            action = "create"
            try:
                with transaction.atomic():
                    room, created = Room.objects.get_or_create(
                        name=track["title"],
                        conference_id=conferences[track["conference"]],
                    )
                    if not created:
                        action = "skip"
            except Exception as exc:
                msg = (
                    f"Something bad happened when importing track/room "
                    f'{track["title"]}: {exc}'
                )
                self.stdout.write(self.style.NOTICE(msg))
                action = "error"
                continue
            finally:
                actions[action] += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Rooms: "
                f'{actions["create"]} created, '
                f'{actions["update"]} updated, '
                f'{actions["skip"]} skipped, '
                f'{actions["error"]} errors.'
            )
        )

    def db_connect(self, options):
        db_path = options["db_path"]
        if not db_path:
            self.stdout.write(
                self.style.NOTICE("DB path not specified, using default.")
            )
            db_path = DEFAULT_DB_PATH
        self.stdout.write(f"Using DB: {db_path}")

        conn = sqlite3.connect(db_path)
        conn.row_factory = dict_factory
        self.c = conn.cursor()

    def handle(self, *args, **options):
        self.stdout.write("Starting...")

        self.db_connect(options)

        entities = "all"
        overwrite = False
        if options["entities"]:
            entities = options["entities"].split(",")
            overwrite = options["overwrite"]
        elif options["overwrite"]:
            raise CommandError("Cannot overwrite without --entities parameter")

        if overwrite:
            self.stdout.write(
                self.style.NOTICE(
                    "This command will overwrite entities in the destination DB!!!"
                )
            )

        if "user" in entities or entities == "all":
            self.import_users(overwrite=overwrite)
        if "submission_type" in entities or entities == "all":
            self.create_submission_types(overwrite=overwrite)
        if "topic" in entities or entities == "all":
            self.create_topics(overwrite=overwrite)
        if "conference" in entities or entities == "all":
            self.import_conferences(overwrite=overwrite)
        if "room" in entities or entities == "all":
            self.import_rooms(overwrite=overwrite)
        if "submission" in entities or entities == "all":
            self.import_submissions(overwrite=overwrite)
        if (
            "schedule_item" in entities or entities == "all"
        ):  # needs submission and room
            self.import_schedule_items(overwrite=overwrite)

        self.stdout.write(self.style.SUCCESS("Done!"))
