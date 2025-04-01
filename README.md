SETUP INSTRUCTIONS:

1. Create a MySQL database:
   $ mysql -u root -p
   mysql> CREATE DATABASE online_exam_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   mysql> quit

2. Install required packages:
   $ pip install django mysqlclient crispy-forms crispy-bootstrap4

3. Set up the Django project:
   $ django-admin startproject online_exam_system
   $ cd online_exam_system
   $ python manage.py startapp exam_app

4. Copy all the code to the appropriate files in your project structure

5. Make and apply migrations:
   $ python manage.py makemigrations
   $ python manage.py migrate

6. Create a superuser:
   $ python manage.py createsuperuser

7. Run the development server:
   $ python manage.py runserver

8. Access the application at http://127.0.0.1:8000/
   Admin interface: http://127.0.0.1:8000/admin/