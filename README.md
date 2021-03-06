# Planeks-Test-Task
Simple news site built with Django

# To run locally
Register at [Mailgun](https://www.mailgun.com/) and get your API key and Domain ([details](https://documentation.mailgun.com/en/latest/))

Set up [broker](https://docs.celeryproject.org/en/latest/getting-started/brokers/) you like for celery to use

Configure required environment variables:
+ BROKER_URL
+ MAILGUN_API_KEY
+ MAILGUN_DOMAIN

Apply migrations
```python
manage.py migrate
```

Then run **create_default_groups** manage.py command to create default permission groups
```python
python manage.py create_default_groups
```

Now you are able to test application on your local machine
```python
python manage.py runserver
```
