# Sheryians Website Clone using Django

This project is a Sheryians Website Clone developed using Python, Django, HTML, CSS, JavaScript, and SQL.

I built this project as an online learning platform where students can register, log in, explore courses, enroll in courses, and manage their profiles. The application also includes admin functionality for managing courses, mentors, and course modules.

## Technologies Used

- Python
- Django
- Django ORM
- SQL
- HTML
- CSS
- JavaScript
- Bootstrap
- Git & GitHub

## Features

- User Registration and Login
- User Authentication and Logout
- Student Profile Management
- Course Listing and Course Details
- Course Enrollment
- Payment Flow
- Course Modules and Lessons
- Session and Cookie Management
- Form Validation
- Role-Based Access Control
- Admin Course and Mentor Management

## Project Workflow

1. Users can register and log in to the website.
2. Students can explore available courses and view course details.
3. Students can select a course and proceed to enrollment.
4. The application processes the payment flow and records enrollment.
5. Enrolled students can view their courses through their profiles.
6. Admin users can add, update, and manage courses, mentors, and modules.
7. Django ORM handles database operations.

## Project Structure

```text
sheryians/
│
├── manage.py
├── project/
├── application/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
├── templates/
├── static/
├── media/
└── README.md
```

## How to Run

**1. Clone the repository**

```bash
git clone https://github.com/SachinDevarajan/sheryians.git
cd sheryians
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Configure the database**

Update your database settings and environment variables according to your local setup.

**4. Apply database migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Run the development server**

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## What I Learned

Through this project, I gained practical experience in:

- Django MVT Architecture
- Django Models and ORM
- User Authentication and Authorization
- Sessions and Cookies
- Form Handling and Validation
- CRUD Operations
- Database Relationships
- Role-Based Permissions
- Integrating Frontend with Django
- Building an Online Course Management System

## Author

**Sachin Devarajan**

GitHub: [SachinDevarajan](https://github.com/SachinDevarajan)

LinkedIn: [Sachin Devarajan](https://www.linkedin.com/in/sachindevarajan)