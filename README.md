# Django Beginner Notes
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\activate

## Environment Setup

### Creating Virtual Environment with UV
```bash
# Install uv
pip install uv

# Create virtual environment
uv venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

# Install Django
uv pip install django
```

### Create New Project
```bash
# Create project
django-admin startproject projectname

# Go inside project folder
cd projectname

# Create app (optional)
python manage.py startapp appname

# Run server
python manage.py runserver
```

## Project Structure

```
projectname/
├── manage.py                 # Main file to run commands
├── projectname/
│   ├── settings.py          # All configurations
│   ├── urls.py              # Main routing file
│   ├── wsgi.py
│   └── asgi.py
├── appname/
│   ├── views.py             # Logic for each page
│   ├── models.py            # Database tables
│   ├── urls.py              # App-specific routes
│   └── admin.py
├── templates/               # HTML files folder
└── static/                  # CSS, JS, images folder
```

## Core Files Explained

### `manage.py`
Main file that runs everything. You use it for all commands.
```bash
python manage.py runserver        # Start server
python manage.py makemigrations   # Prepare database changes
python manage.py migrate          # Apply database changes
```

### `settings.py`
All project settings live here.

```python
DEBUG = True    # Show errors on page (False in production)

ALLOWED_HOSTS = []    # Empty = only localhost. Add domains for production

BASE_DIR = Path(__file__).resolve().parent.parent    # Project root path

INSTALLED_APPS = [    # All apps in your project
    'django.contrib.admin',
    'appname',    # Add your app here
]

# Template settings
TEMPLATES = [{
    'DIRS': [BASE_DIR / 'templates'],    # Where HTML files are
}]

# Static files settings
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']    # Where CSS/JS files are
```

### `urls.py` 
Routing - connects URLs to views.

**Main urls.py:**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('appname.urls')),    # Include app urls
]
```

**App urls.py:**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]
```

### `views.py`
Main logic for each page. What happens when user visits a URL.

```python
from django.http import HttpResponse
from django.shortcuts import render

# Simple text response
def home(request):
    return HttpResponse("Hello World")

# HTML template response
def about(request):
    return render(request, 'about.html')

# Template with data
def profile(request):
    context = {
        'name': 'John',
        'age': 25
    }
    return render(request, 'profile.html', context)
```

### `models.py`
Database structure. Each class = one table.

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# After creating model, run:
# python manage.py makemigrations
# python manage.py migrate
```

## Working with Templates

### Create templates folder
Create `templates/` folder in project root (same level as manage.py).

### Basic HTML template
**templates/home.html:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Home Page</title>
</head>
<body>
    <h1>Welcome</h1>
</body>
</html>
```

### Template with variables
**views.py:**
```python
def home(request):
    context = {'username': 'John'}
    return render(request, 'home.html', context)
```

**templates/home.html:**
```html
<h1>Hello {{ username }}</h1>
```

## Working with Static Files (CSS/JS)

### Setup static folder
1. Create `static/` folder in project root
2. Inside static, create: `css/`, `js/`, `images/` folders
3. Add to `settings.py`:
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### Use static files in template
**templates/home.html:**
```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <h1>Hello</h1>
    <img src="{% static 'images/logo.png' %}" alt="Logo">
    <script src="{% static 'js/script.js' %}"></script>
</body>
</html>
```

**Important:** Always write `{% load static %}` at the very top before using any `{% static '...' %}`

---

# ERRORS & SOLUTIONS

## Error 1: TemplateDoesNotExist

**Full Error:**
```
TemplateDoesNotExist at /
home.html
```

**Why it happens:**
- templates folder not created
- Wrong path in `settings.py`
- Wrong template name in views.py

**Solution:**
1. Check `settings.py`:
```python
TEMPLATES = [{
    'DIRS': [BASE_DIR / 'templates'],  # Must point to templates folder
}]
```
2. Make sure folder name is exactly `templates`
3. Make sure file name matches: `render(request, 'home.html')` and file is `home.html`

---

## Error 2: Static Files Not Loading (CSS/JS not working)

**What you see:**
- Page loads but no styling
- Images don't show
- JavaScript doesn't work

**Why it happens:**
- Forgot `{% load static %}` in template
- Wrong `STATICFILES_DIRS` in settings.py
- Wrong folder structure

**Solution:**
1. **Always add this at TOP of HTML file:**
```html
{% load static %}
```

2. **Check settings.py:**
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Must point to static folder
```

3. **Check folder structure:**
```
project/
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   └── images/
└── templates/
```

4. **Use correct path in template:**
```html
{% static 'css/style.css' %}    ✓ Correct
{% static 'style.css' %}         ✗ Wrong (missing css folder)
```

---

## Error 3: Page Not Found (404)

**Full Error:**
```
Page not found (404)
Request URL: http://127.0.0.1:8000/about/
```

**Why it happens:**
- URL not added in `urls.py`
- Wrong URL pattern
- Forgot to include app urls

**Solution:**
1. **Check app urls.py exists and has pattern:**
```python
urlpatterns = [
    path('about/', views.about, name='about'),
]
```

2. **Check main urls.py includes app urls:**
```python
from django.urls import path, include

urlpatterns = [
    path('', include('appname.urls')),
]
```

3. **URL patterns:**
```python
path('about/', ...)     # URL: /about/
path('', ...)           # URL: / (homepage)
path('blog/post/', ...) # URL: /blog/post/
```

---

## Error 4: ModuleNotFoundError

**Full Error:**
```
ModuleNotFoundError: No module named 'appname'
```

**Why it happens:**
- App not added to `INSTALLED_APPS` in settings.py

**Solution:**
Add your app in `settings.py`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appname',    # Add this
]
```

---

## Error 5: ImportError in views

**Full Error:**
```
ImportError: cannot import name 'HttpResponse' from 'django.http'
```

**Why it happens:**
- Forgot to import at top of file

**Solution:**
Add imports at top of `views.py`:
```python
from django.http import HttpResponse
from django.shortcuts import render
```

---

## Error 6: TemplateSyntaxError (forgot to load static)

**Full Error:**
```
TemplateSyntaxError at /
Invalid block tag: 'static'
```

**Why it happens:**
- Used `{% static '...' %}` without loading it first

**Solution:**
Add at TOP of HTML file:
```html
{% load static %}
<!DOCTYPE html>
...
```

---

## Error 7: View function not found

**Full Error:**
```
AttributeError: module 'appname.views' has no attribute 'home'
```

**Why it happens:**
- Function name in `urls.py` doesn't match `views.py`
- Typo in function name

**Solution:**
Make sure names match:

**urls.py:**
```python
path('', views.home),    # Function name is 'home'
```

**views.py:**
```python
def home(request):    # Function name must be 'home'
    return render(request, 'home.html')
```

---

## Error 8: Path must be BASE_DIR / not BASE_DIR +

**Full Error:**
```
TypeError: unsupported operand type(s) for +: 'Path' and 'str'
```

**Why it happens:**
- Used `+` instead of `/` for path

**Solution:**
```python
# Wrong
STATICFILES_DIRS = [BASE_DIR + 'static']

# Correct
STATICFILES_DIRS = [BASE_DIR / 'static']
```

---

## Error 9: Forbidden (403) CSRF verification failed

**Why it happens:**
- Form submitted without CSRF token

**Solution:**
Add in forms:
```html
<form method="POST">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

---

## Error 10: No such table (database error)

**Full Error:**
```
django.db.utils.OperationalError: no such table: appname_modelname
```

**Why it happens:**
- Created model but didn't migrate

**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Basic Workflow Summary

1. **Create URL** → `urls.py`
2. **Create view function** → `views.py`
3. **Create template** → `templates/filename.html`
4. **Add static files** → `static/css/`, `static/js/`
5. **Load static in template** → `{% load static %}`
6. **Run server** → `python manage.py runserver`
7. **Visit** → `http://127.0.0.1:8000/`