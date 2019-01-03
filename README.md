# Warsztaty_3_rezerwacje

1. cd to the directory of repository.
2. activate your virtualenv.
3. run: `pip install -r requirements.txt` in your shell.
4. run: `python3 manage.py createsuperuser` for django admin (optional, it will make admin account on `/admin` webpage).
5. run: `python3 manage.py makemigrations`.
6. run: `python3 manage.py migrate`.
7. run: `python3 manage.py runserver` it will set up server on localhost. Add `<ip>:<port>` to command for development server.

Database is set up as SQLite, change it for development use.
