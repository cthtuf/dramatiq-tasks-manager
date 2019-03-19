from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from dramatiq_tasks_manager.permissions import TASKS_GROUPS


class Command(BaseCommand):
    help = "Create test user."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.UserModel = get_user_model()
        self.username_field = self.UserModel._meta.get_field(self.UserModel.USERNAME_FIELD)

    def add_arguments(self, parser):
        parser.add_argument(
            "--username", "-u",
            type=str,
            help="Username",
            dest="username",
            default="testuser",
        )

        parser.add_argument(
            "--email", "-e",
            type=str,
            help="Email",
            dest="email",
            default="test@ema.il",
        )

        parser.add_argument(
            "--password", "-p",
            type=str,
            help="Password",
            dest="password",
            default="testpassword",
        )

    def handle(self, *args, **options):
        username = options[self.UserModel.USERNAME_FIELD]
        email = options['email']
        password = options['password']

        user = self.UserModel._default_manager.db_manager("default").create_user(
            username=username,
            email=email,
            password=password,
        )

        for group_name in TASKS_GROUPS:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        self.stdout.write(f'* Created testuser with username={username}, password={password}')
