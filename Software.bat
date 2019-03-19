@echo off

start chrome http://localhost:8000/

cmd /k "cd /d C:\Users\Niamatullah Saryabi\Envs\bhatta_3\Scripts & activate & cd /d    G:\batta_management & python manage.py runserver"
