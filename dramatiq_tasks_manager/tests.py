import json
from collections import namedtuple
from datetime import datetime
from enum import Enum

from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from .permissions import GROUP_TASK_EXECUTORS, GROUP_TASK_REPORTERS, GROUP_TASK_SCHEDULERS


class ValidationErrorMessages(Enum):
        unknown_trigger = 'Unknown trigger'
        field_required = 'This field is required'
        unknown_actor = 'Unknown actor name'


class TasksTestCase(APITestCase):
    def login(self, user):
        """
        Wrapper for self.client.login
        :param user:
        :return:
        """
        return self.client.login(username=user.username,
                                 password=user.password)

    def get(self, path_name):
        """
        Wrapper for self.client.get
        :param path_name:
        :return:
        """
        return self.client.get(reverse_lazy(path_name))

    def post(self, path_name, data=None):
        """
        Wrapper for self.client.post
        :param path_name:
        :param data:
        :return:
        """
        return self.client.post(reverse_lazy(path_name), json.dumps(data), content_type='application/json')

    def put(self, path_name, data=None):
        """
        Wrapper for self.client.post
        :param path_name:
        :param data:
        :return:
        """
        return self.client.put(reverse_lazy(path_name), json.dumps(data), content_type='application/json')

    def patch(self, path_name, data=None):
        """
        Wrapper for self.client.post
        :param path_name:
        :param data:
        :return:
        """
        return self.client.patch(reverse_lazy(path_name), json.dumps(data), content_type='application/json')

    def setUp(self):
        UserDataClass = namedtuple('UserData', ('username', 'email', 'password'))
        self.user_wo_groups_data = UserDataClass(username="1testuser",
                                                 email="1test@ema.il",
                                                 password="1testpassword")
        self.user_reporter_data = UserDataClass(username="2testuser",
                                                email="2test@ema.il",
                                                password="2testpassword")
        self.user_executor_data = UserDataClass(username="3testuser",
                                                email="3test@ema.il",
                                                password="3testpassword")
        self.user_scheduler_data = UserDataClass(username="4testuser",
                                                 email="4test@ema.il",
                                                 password="4testpassword")
        self.user_wo_groups = User.objects.create_user(username=self.user_wo_groups_data.username,
                                                       email=self.user_wo_groups_data.email,
                                                       password=self.user_wo_groups_data.password)
        self.user_reporter = User.objects.create_user(username=self.user_reporter_data.username,
                                                      email=self.user_reporter_data.email,
                                                      password=self.user_reporter_data.password)
        self.group_reporter = Group.objects.get(name=GROUP_TASK_REPORTERS)
        self.user_reporter.groups.add(self.group_reporter)
        self.user_executor = User.objects.create_user(username=self.user_executor_data.username,
                                                      email=self.user_executor_data.email,
                                                      password=self.user_executor_data.password)
        self.group_executor = Group.objects.get(name=GROUP_TASK_EXECUTORS)
        self.user_executor.groups.add(self.group_executor)

        self.user_scheduler = User.objects.create_user(username=self.user_scheduler_data.username,
                                                       email=self.user_scheduler_data.email,
                                                       password=self.user_scheduler_data.password)
        self.group_scheduler = Group.objects.get(name=GROUP_TASK_SCHEDULERS)
        self.user_scheduler.groups.add(self.group_scheduler)

    def test_list_executed_tasks(self):
        # Negative
        self.assertTrue(self.login(self.user_wo_groups_data))
        response = self.get('task_executed_list')
        self.assertEqual(403, response.status_code)

        # User with group reporter
        self.assertTrue(self.login(self.user_reporter_data))
        response = self.get('task_executed_list')
        self.assertEqual(200, response.status_code)

        # User with group executor
        self.assertTrue(self.login(self.user_executor_data))
        response = self.get('task_executed_list')
        self.assertEqual(200, response.status_code)

    def test_execute_permissions(self):
        self.assertTrue(self.login(self.user_wo_groups_data))
        response = self.post('task_execute')
        self.assertEqual(403, response.status_code)

        # User with group reporter
        self.assertTrue(self.login(self.user_reporter_data))
        response = self.post('task_execute')
        self.assertEqual(403, response.status_code)

        # User with group scheduler
        self.assertTrue(self.login(self.user_scheduler_data))
        response = self.post('task_execute')
        self.assertEqual(403, response.status_code)

    def test_execute_disallowed_methods(self):
        # User with group executor
        self.assertTrue(self.login(self.user_executor_data))
        # Check for incorrect request methods
        response = self.get('task_execute')
        self.assertEqual(405, response.status_code)
        response = self.put('task_execute')
        self.assertEqual(405, response.status_code)
        response = self.patch('task_execute')
        self.assertEqual(405, response.status_code)

    def test_execute_task(self):
        # User with group executor
        self.assertTrue(self.login(self.user_executor_data))
        # Request wo data
        response = self.post('task_execute')
        self.assertEqual(400, response.status_code)

        # Request with incorrect actor name
        execute_request_data = {
            "actor_name": "some_actor"
        }
        response = self.post('task_execute', data=execute_request_data)
        self.assertEqual(400, response.status_code)
        self.assertContains(response, ValidationErrorMessages.unknown_actor.value, status_code=400)

    def test_schedule_permissions(self):
        self.assertTrue(self.login(self.user_wo_groups_data))
        response = self.post('task_schedule')
        self.assertEqual(403, response.status_code)

        # User with group reporter
        self.assertTrue(self.login(self.user_reporter_data))
        response = self.post('task_schedule')
        self.assertEqual(403, response.status_code)

        # User with group executor
        self.assertTrue(self.login(self.user_executor_data))
        response = self.post('task_schedule')
        self.assertEqual(403, response.status_code)

    def test_schedule_disallowed_methods(self):
        # User with group scheduler
        self.assertTrue(self.login(self.user_scheduler_data))
        # Check for incorrect request methods
        response = self.get('task_schedule')
        self.assertEqual(405, response.status_code)
        response = self.put('task_schedule')
        self.assertEqual(405, response.status_code)
        response = self.patch('task_schedule')
        self.assertEqual(405, response.status_code)

    def test_schedule_task(self):
        # User with group scheduler
        self.assertTrue(self.login(self.user_scheduler_data))
        # Request wo data
        response = self.post('task_schedule')
        self.assertEqual(400, response.status_code)

        # Request witout trigger
        execute_request_data = {
            "actor_name": "some_actor"
        }
        response = self.post('task_schedule', data=execute_request_data)
        self.assertContains(response, ValidationErrorMessages.unknown_trigger.value, status_code=400)

        # Request without run_date for date trigger
        execute_request_data = {
            "actor_name": "some_actor",
            "trigger": "date",
        }
        response = self.post('task_schedule', data=execute_request_data)
        self.assertContains(response, ValidationErrorMessages.field_required.value, status_code=400)

        # Request with unknown actor for date trigger
        execute_request_data = {
            "actor_name": "some_actor",
            "trigger": "date",
            "run_date": datetime.now().isoformat()
        }
        response = self.post('task_schedule', data=execute_request_data)
        self.assertContains(response, ValidationErrorMessages.unknown_actor.value, status_code=400)

        # Request without date data for interval trigger
        execute_request_data = {
            "actor_name": "some_actor",
            "trigger": "interval",
        }
        response = self.post('task_schedule', execute_request_data)
        self.assertContains(response, ValidationErrorMessages.unknown_actor.value, status_code=400)
