from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType


def create_addition_admin_log_entry(user, obj, change_message=""):
    create_admin_log_entry(
        user=user, obj=obj, action_flag=ADDITION, change_message=change_message
    )


def create_change_admin_log_entry(user, obj, change_message=""):
    create_admin_log_entry(
        user=user, obj=obj, action_flag=CHANGE, change_message=change_message
    )


def create_deletion_admin_log_entry(user, obj, change_message=""):
    create_admin_log_entry(
        user=user, obj=obj, action_flag=DELETION, change_message=change_message
    )


def create_admin_log_entry(user, obj, action_flag, change_message=""):
    """
    Creates a log entry in the Django admin audit log.

    :param user: The user object who is responsible for the action.
    :param obj: The object that was added/changed/deleted.
    :param action_flag: The type of action (ADDITION, CHANGE, DELETION).
    :param change_message: A message describing the change.
    """
    LogEntry.objects.create(
        user_id=user.pk,
        content_type_id=ContentType.objects.get_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=action_flag,
        change_message=change_message,
    )
