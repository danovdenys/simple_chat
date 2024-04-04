# Simple Chat Application

This is a simple chat application built for the iSi Technology test assignment. It allows users to send and receive messages in real-time.

## Installation

Follow these steps to install and run the application:

1. Clone this repository to your local machine using the following command: 
    ```
    git clone https://github.com/danovdenys/simple_chat
    ```
2. Navigate to the project directory:
    ```
    cd /path/to/your/project
    ```
3. Create a virtual environment:
    ```
    python3 -m venv env
    ```
4. Activate the virtual environment:
    ```
    source env/bin/activate
    ```
5. Install the required dependencies from the `requirements.txt` file:
    ```
    pip install -r requirements.txt
    ```
6. Load the initial data into the application using the Django's `loaddata` command:
    ```
    python manage.py loaddata fixtures.json
    ```
7. Run the application. You can use Django's development server:
    ```
    python manage.py runserver
    ```
    Or you can use Docker Compose if you have it installed:
    ```
    docker-compose up
    ```

## Testing 
To test the application, follow these steps:

1. Make sure you are in the project directory and your virtual environment is activated.

2. Run Django's built-in test command:
    ```
    python manage.py test
    ```
This command will automatically find all the test files in your project (those whose names begin with `test`), and run the test cases defined in them.

3. If you want to run tests for a specific app, you can specify it in the command. For example, to run tests for an app named `posts`, you would use:
    ```
    python manage.py test posts
    ```
4. After running the tests, you will see the test results in the console. If any tests fail, you will see error messages explaining what went wrong.
