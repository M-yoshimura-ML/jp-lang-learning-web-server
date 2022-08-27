# Architecture:

### Frameworks:

-   Server Side Framework: `Django 3.1`, `djangorestframework 3.11.1`

### System Requirements:

-   Python >=3.8

### Packages Installed

- Authentication:

    - `"djangorestframework-simplejwt"`
  
- Others:
  - See requirements-dev.txt

# Getting Started

1. Clone Repository

    `git clone https://github.com/M-yoshimura-ML/jp-lang-learning-web-server.git`

2. Create virtual env in your local(recommend to use Anaconda) 

3. Install package dependencies for requirements-dev.txt in virtual env

    `pip install`

4. Migrations and Migrate

    `python manage.py makemigrations`, `python manage.py migrate` 


5. Create Superuser
   `python manage.py createsuperuser`

6. Begin Local Web Server from virtual env

    `python manage.py runserver` or start from PyCharm IDE


7. Open your browser `http://127.0.0.1:8000/api` or `http://127.0.0.1:8000/admin`
