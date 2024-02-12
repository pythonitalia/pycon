from custom_admin.audit import (
    create_addition_admin_log_entry,
    create_change_admin_log_entry,
    create_deletion_admin_log_entry,
)
from django.contrib.admin.models import LogEntry
import pytest
from schedule.tests.factories import ScheduleItemFactory


pytestmark = pytest.mark.django_db


def test_create_audit_log_for_creation(admin_user):
    obj = ScheduleItemFactory()
    create_addition_admin_log_entry(admin_user, obj, change_message="Test")

    log_entry = LogEntry.objects.get()

    assert log_entry.action_flag == LogEntry.ADDITION
    assert log_entry.object_id == obj.pk
    assert log_entry.user == admin_user


def test_create_change_admin_log_entry(admin_user):
    obj = ScheduleItemFactory()
    create_change_admin_log_entry(admin_user, obj, change_message="Test")

    log_entry = LogEntry.objects.get()

    assert log_entry.action_flag == LogEntry.ADDITION
    assert log_entry.object_id == obj.pk
    assert log_entry.user == admin_user


def test_create_deletion_admin_log_entry(admin_user):
    obj = ScheduleItemFactory()
    create_deletion_admin_log_entry(admin_user, obj, change_message="Test")

    log_entry = LogEntry.objects.get()

    assert log_entry.action_flag == LogEntry.ADDITION
    assert log_entry.object_id == obj.pk
    assert log_entry.user == admin_user
