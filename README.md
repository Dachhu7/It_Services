# IT Services

## Description

The IT Services project is a Django-based web application designed to manage IT services, subscriptions, and user interactions. The application features a user-friendly interface, service management, and integration with Razorpay for payments.

## Features

- **Home View**: Displays available services with an option to subscribe.
- **Service Management**: CRUD operations for service details with activation toggles.
- **Subscription Management**: Users can subscribe to services, input address details, and complete payments.
- **User Authentication**: Registration, login, and access control for certain views.
- **Payment Integration**: Razorpay API for handling payments and callbacks.
- **Bootstrap Integration**: For responsive and modern UI design.
- **Email API**: Configured for user registration with OTP verification.

## How to Run

1. **Clone the Repository**

   ```bash
   git clone <repository-url>

2. **Navigate to the Project Directory**

    ```bash
    cd it-services

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt

4. **Apply Migrations**

    ```bash
    python manage.py migrate

5. **Create a Superuser**

   ```bash
   python manage.py createsuperuser


6. **Run the Development Server**

    ```bash
    python manage.py runserver

7. **Access the Application**

    ```bash
    Open your browser and navigate to http://127.0.0.1:8000/ to view the application

## Requirements
- Python 3.8
- Django 3.2
- Razorpay
- Bootstrap

## File Structure
- `/project_root`: Root directory containing the manage.py file and project settings.
- `/services`: Django app for managing services and subscriptions.
- `/templates`: HTML templates for various views.
- `/static`: Static files including CSS and JavaScript.
- `/migrations`: Database migrations files.

## Author
[Darshan Kudache](https://www.linkedin.com/in/darshan-kudache-a4369328b)