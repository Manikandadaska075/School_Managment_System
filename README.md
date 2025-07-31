# Creating a Project

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
    