# Resto Commerce App
manage orders for resto-bar's

![python3.8](https://img.shields.io/badge/python-v3.8-blue)
![django2.2](https://img.shields.io/badge/django-v2.2-blue)
![winx86/64](https://img.shields.io/badge/OS-win%20x86%2Fx64-lightgrey)
![winx86/64](https://img.shields.io/badge/license-GPL%20v3-brightgreen)

## Project install

- Install python 3.8 (or high) x64 adding to PATH

- Install git (if don't have it)

- Clone this repository:
```bash
> git clone https://github.com/lucaslucyk/resto-commerce.git
> cd resto-commerce
```

- Install dependencies:
```bash
> python -m pip install requirements.txt -r
```

- Generate and run migrations:
```bash
> python manage.py makemigrations
> python manage.py migrate
```

- (ERROR ONLY) Repare conection between poroject and database:
```bash
> python manage.py migrate --run-syncdb
```

- Create superuser completing specific data:
```bash
> python manage.py createsuperuser
...
```

- Run server:
```bash
> python manage.py runserver
```

- For stop server, use CTRL+C.

*\* To use a third party database or web-server, use the corresponding settings* 

**\* Scheduled tasks don't work on UNIX OS's**

## Application Guide
...

