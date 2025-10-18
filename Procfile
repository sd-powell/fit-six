release: python manage.py collectstatic --noinput --clear
web: gunicorn fitsix_project.wsgi:application