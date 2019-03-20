============
Description
============
This package provides API interface for executing and scheduling tasks. Look through this examples of requests to API.

1. Get list of executed tasks:


    curl -X GET http://localhost:8000/executed -H 'Content-Type: application/json'


2. Get details of the executed task (It will show result of task if result backend was used and TTL not expired):


    curl -X GET http://localhost:8000/executed/:message_id -H 'Content-Type: application/json'


3. Execute task:


    curl -X POST http://localhost:8000/execute -H 'Content-Type: application/json' -d '{"actor_name": "print_result", "kwargs": {"message_data": {"message_id": "123456789"},"result": "This actor is almost useless for direct calling. Use it as success-callback for other actors."}}'


4. Schedule task on certain time:


    curl -X POST http://localhost:8000/schedule/by_date -H 'Content-Type: application/json' -d '{"actor_name": "print_resulst","run_date": "2019-02-11T07:31:00Z","kwargs": {"message_data": {"message_id": "123456789"},"result": "This actor is almost useless for direct calling. Use it as success-callback for other actors."}}'


5. Get list of scheduled tasks


    curl -X GET http://localhost:8000/scheduled -H 'Content-Type: application/json'


============
Requirements
============
1. dramatiq
2. django_dramatiq
3. apscheduler
