# luenelock-api

![SAST](https://github.com/xenobyte/luenelock-api/actions/workflows/sast.yml/badge.svg) ![CI](https://github.com/xenobyte/luenelock-api/actions/workflows/django.yml/badge.svg)

This is an open source project designed for university students who want to learn about DevSecOps topics. The project is written in Python and provides a REST API to simulate interaction with fictitious smart locks.

Please note that this project is for educational purposes only and should not be used in production environments. The smart locks used in this project are purely fictional and should not be used for real-world security purposes.

## Installation

To install the DevSecOps Smart Locks REST API, follow these steps:

1.) Clone the repository to your local machine using Git:

```bash
git clone git@github.com:xenobyte/luenelock-api.git && cd luenelock-api
```

2.) Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

3.) Prepare the database
```bash
python manage.py migrate
```

## Usage

Start the development server with the following command:

```bash
python manage.py runserver
```

open `http://localhost:8000/api/locks` in your browser.

### Administration

Create an administrator account with the following command

```bash
python manage.py createsuperuser
```

then you can access the system admininistration `http://localhost:8000/admin` with that account.
