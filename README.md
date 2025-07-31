# School Management System

1. Create a folder, name it appropriately, open the folder in VS Code, and run the following command in the terminal to create a virtual environment (you can choose your own name for the environment):
    ```
    python -m venv env
    ```

2. Activate the virtual environment by running the command (replace env with your environment name if different):
    ```
    .\env\Scripts\activate
    ```

3. Install the required packages from requirements.txt:
    ```
    pip install -r requirements.txt
    ```

4. Create the main Django project by running: 
    ```
    django-admin startproject school_management
    ```

5. Create a sub-apps using the command:
    ```
    python manage.py startapp user

    python manage.py startapp Academic
    ```

6. Register the sub-app:
    Open settings.py in the main project folder (school_management) and add 'user' and 'Academic' to the INSTALLED_APPS list.

7. Define your models:
    Open models.py inside the user and Academic app and define the database tables you need.

8. Apply the migrations:
    Run the following commands to create and apply the database migrations:
    ```
    python manage.py makemigrations 

    python manage.py migrate
    ```

9. To start the Django development server, run the following command:
    ```
    python manage.py runserver
    ```
    
10. API Endpoints In postman:

    1. Admin Registration:
        Post: 127.0.0.1:8000/AdminRegistration/
        ```
        {
        "username": "admin",
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User",
        "password": "12345"
        }
        ```

    2. Admin Login:
        Post: 127.0.0.1:8000/AdminLogin/
        ```
        {
        "username": "admin",
        "password": "12345"
        }
        ```

    3. Department Creation By Admin:
        Post: 127.0.0.1:8000/CreateDepartmentByAdmin/

        Copy the access token from the admin login and paste it in the Authorization header using Bearer Token type.
        ```
        {
        "subject_code": "ME103",
        "department_name": "Mechanics",
        "subject": "Machine design"
        }
        ```

    4. Teacher or Student Registration By Admin:
        Post: 127.0.0.1:8000/RegistrationByAdmin/

        Copy the access token from the admin login and paste it in the Authorization header using Bearer Token type.
        ```
        {
        "username": "teacher001",
        "email": "teach001@example.com",
        "first_name": "Arun",
        "last_name": "R",
        "password": "12345",
        "user_type": "teacher",
        "address": "123 School Lane",
        "department": "Computer Science",
        "position": "teacher",
        "subject": "Python"
        }
        {
        "username": "student005",
        "email": "stud005@example.com",
        "first_name": "Sachin",
        "last_name": "R",
        "password": "12345",
        "user_type": "student",
        "address": "321 Scholar Avenue",
        "department": "Computer Science"
        }
        ```

    5. Delete user by Admin
        Delete: 127.0.0.1:8000/delete-userbyadmin/

        Copy the access token from the admin login and paste it into the Authorization header using the Bearer Token type.
        In the Params section, provide two keys: user_id and user_type.

        - user_id refers to the ID of the user who should be deleted.

        - user_type specifies the type of user (e.g., student, teacher, admin) to which the user belongs.

    6. Teacher Login
        Post: 127.0.0.1:8000/TeacherLogin/
        ```
        {
        "username": "teacher002",
        "password": "12345"
        }
        ```

    7. Teacher Profile View
        Get: 127.0.0.1:8000/teacherprofileview/

        Copy the access token from the teacher login and paste it into the Authorization header using the Bearer Token type.

    8. The HOD can view student details for their corresponding department.
        Get: 127.0.0.1:8000/StudentlistviewByHOD/  

        Copy the access token from the teacher login and paste it into the Authorization header using the Bearer Token type.

    9. The teacher can view student details for their corresponding department subject.
        Get: 127.0.0.1:8000/DepartmentStudentList/

        Copy the access token from the teacher login and paste it into the Authorization header using the Bearer Token type.

    10. The teacher can add,update student mark for their corresponding department subject.
        Put: 127.0.0.1:8000/UpdateStudentMarksByTeacherOrAdmin/

        Copy the access token from the teacher login and paste it into the Authorization header using the Bearer Token type.

        In the Params section, provide two keys: student_id and mark.

        - student_id refers to the ID of the student whose mark should be updated.

        - mark specifies the mark to be assigned to the student for that particular subject.

    11. Student login
        Post: 127.0.0.1:8000/Studentlogin/
        ```
        {
        "username": "student004",
        "password": "12345"
        }
        ```

    12. Student profile view
        Get: 127.0.0.1:8000/studentprofileview/

        Copy the access token from the student login and paste it into the Authorization header using the Bearer Token type.

    13. Student can view there mark of each subject
        Get: 127.0.0.1:8000/student-total-marks/

        Copy the access token from the student login and paste it into the Authorization header using the Bearer Token type.
        
        In the Params section, provide one keys: student_id

        - student_id refers to the ID of the student 

    14. Teacher can view all the student mark of there curresponding department subject
        Get: 127.0.0.1:8000/teacher-subject-marks/

        Copy the access token from the teacher login and paste it into the Authorization header using the Bearer Token type.

    15. HOD can view all the student mark status of there curresponding department
        Get: 127.0.0.1:8000/department-stats/

        Copy the access token from the teacher login and paste it into the Authorization header using the Bearer Token type.







