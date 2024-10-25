**TECH STACK**
Backend: Django, Django REST Framework
Database: SQLite
Frontend: Bootstrap, Select2
API Documentation: drf-yasg


**PREREQUISITES**
Before you begin, ensure you have the following installed:
Python 3.8 or higher
pip (Python package manager)
Django==4.2.10
djangorestframework==3.14.0
and all the installs from requirements.txt file


**SET UP THE DATABASE**
- python manage.py makemigrations  
- python manage.py migrate


**CREATE SUPERUSER**
- python manage.py createsuperuser
 (Or use existing user id - Admin, pswd - Admin)


**RUN THE DEVELOPMENT SERVER**
- python manage.py runserver

**RULE SYNTAX**
Rules can be written using a simple syntax. Here are some examples:

   amount > 1000
   (category == "electronics") AND (price < 500)
   (status == "active") AND (age > 18 OR (parent_consent == true))

  



