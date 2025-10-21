# Django Authentication System

A comprehensive Django project implementing user registration, login, logout, and dashboard access with Bootstrap styling, flash messages, and robust error handling.

## Features

- **User Registration & Login**: Secure user registration and authentication
- **Custom User Model**: Extended user model with additional fields
- **Password Reset**: Complete password reset functionality
- **Flash Messages**: User feedback system with Bootstrap styling
- **Protected Dashboard**: Login-required dashboard page
- **Bootstrap 5 UI**: Modern, responsive user interface
- **Comprehensive Testing**: Full test coverage for all authentication flows
- **Error Handling**: Robust error handling and logging
- **Environment Configuration**: Secure configuration management

## Installation & Running

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file with your configuration:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Start the server: `python manage.py runserver`
8. Run tests: `python manage.py test`

## Testing

The project includes comprehensive test coverage:
- Authentication flow tests
- Form validation tests
- Password reset tests
- Error handling tests

Run tests with: `python manage.py test`

## Security Features

- CSRF protection
- Password validation
- Secure session management
- Environment-based configuration
- Input validation and sanitization

## Future Improvements

- Email verification on registration
- Two-factor authentication
- User profile management
- API endpoints with Django REST Framework
- Docker containerization
