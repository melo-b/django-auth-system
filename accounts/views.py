from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import login, get_user_model
from django.db import IntegrityError
import logging
from .forms import RegisterForm

User = get_user_model()

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        try:
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful! Welcome!')
                logger.info(f"New user registered: {user.username}")
                return redirect('dashboard')
            else:
                logger.warning(f"Registration failed for user: {request.POST.get('username', 'unknown')}")
                messages.error(request, 'Please correct the errors below.')
        except IntegrityError as e:
            logger.error(f"Integrity error during registration: {e}")
            messages.error(request, 'Username already exists. Please choose a different username.')
        except ValidationError as e:
            logger.error(f"Validation error during registration: {e}")
            messages.error(request, 'Invalid data provided. Please check your input.')
        except Exception as e:
            logger.error(f"Unexpected error during registration: {e}")
            messages.error(request, 'An unexpected error occurred. Please try again.')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    try:
        logger.info(f"Dashboard accessed by user: {request.user.username}")
        return render(request, 'registration/dashboard.html')
    except Exception as e:
        logger.error(f"Error accessing dashboard for user {request.user.username}: {e}")
        messages.error(request, 'An error occurred while loading the dashboard.')
        return redirect('login')
