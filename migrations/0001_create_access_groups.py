from django.db import migrations

GROUP_TASK_SCHEDULERS = 'TASK_SCHEDULERS'
GROUP_TASK_EXECUTORS = 'TASK_EXECUTORS'
GROUP_TASK_REPORTERS = 'TASK_REPORTERS'
TASKS_GROUPS = (GROUP_TASK_SCHEDULERS, GROUP_TASK_EXECUTORS, GROUP_TASK_REPORTERS)


def create_task_groups(apps, schema_editor):
    group_model = apps.get_model('auth', 'Group')

    for group_name in TASKS_GROUPS:
        _, _ = group_model.objects.get_or_create(name=group_name)


def remove_task_groups(apps, schema_editor):
    group_model = apps.get_model('auth', 'Group')

    for group_name in TASKS_GROUPS:
        group = group_model.objects.filter(name=group_name).first()
        if group:
            group.user_set.clear()
            group.delete()


class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(create_task_groups, remove_task_groups)
    ]
