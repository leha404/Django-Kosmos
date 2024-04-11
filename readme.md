Learning Django. (And "ProstoKosmos")

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

6) Run server:
python manage.py runserver

7) Create SuperUser:
python manage.py createsuperuser

Next: Go to SITE_URL/admin page for auth.
And get working App!