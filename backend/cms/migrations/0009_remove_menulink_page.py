from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('cms', '0008_menu_title'),
    ]

    # The old pages app has been removed: 0006_menu_menulink no longer creates
    # the menulink.page column, so there is no state to change here, only the
    # leftover database objects of already migrated databases to clean up.
    operations = [
        migrations.RunSQL(
            'ALTER TABLE cms_menulink DROP COLUMN IF EXISTS page_id;',
            migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            'DROP TABLE IF EXISTS pages_page;',
            migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            "DELETE FROM django_migrations WHERE app = 'pages';",
            migrations.RunSQL.noop,
        ),
    ]
