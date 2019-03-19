from setuptools import setup

setup(
    name='dramatiq-tasks-manager',
    version='0.0.11',
    packages=['dramatiq_tasks_manager',
              'dramatiq_tasks_manager.management',
              'dramatiq_tasks_manager.management.commands',
              'dramatiq_tasks_manager.migrations',
              ],
    url='https://github.com/cthtuf/dramatiq-tasks-manager',
    license='MIT',
    author='cthtuf',
    author_email='gdazeysinc@gmail.com',
    description='This package provides API interface for executing and scheduling tasks. '
                'It depends on dramatiq and apscheduler',
    install_requires=['APScheduler', 'dramatiq[all]']
)
