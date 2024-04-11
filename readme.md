Learning Django. "Kosmos planner"

Inspired by DjangoGirls:
https://tutorial.djangogirls.org/ru/django/

Instructions:
1) Install virtual env (macOS):
python3 -m venv myvenv

2) Run virtual environment:
source myvenv/bin/activate

3) Update Python package manager:
python3 -m pip install --upgrade pip

4) Get requirement packages (updated requirements.txt):
pip install -r requirements.txt

5) Migrate database:
python manage.py migrate

6) Create SuperUser:
python manage.py createsuperuser

7) Run server:
python manage.py runserver

Next: Go to SITE_URL/admin page for auth.
And get working App!

<!-- Below: instruction to deploy on PythonAnywhere -->
Deploy instruction:

1) Register an account on PythonAnywhere.com
2) Go to Account Tab and create API token if not exists
3) Make a Bash console and follow next instructions:

- pip3.6 install --user pythonanywhere
- pa_autoconfigure_django.py https://github.com/YOUR_GITHUB/YOUR_REPO.git
- cd YOUR_PROJECT_NAME
- python manage.py createsuperuser