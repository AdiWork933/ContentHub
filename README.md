# Portfolio Website - Complete Documentation

A professional, feature-rich portfolio website built with Flask and SQLAlchemy. Manage projects, blog posts, experiences, and tools from an intuitive admin panel.

**Author:** Aditya Choudhary  
**Current Version:** 1.0  
**Last Updated:** January 2026

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Installation & Setup](#installation--setup)
6. [Configuration](#configuration)
7. [Database Models](#database-models)
8. [Admin Panel Guide](#admin-panel-guide)
9. [Public Pages & Routes](#public-pages--routes)
10. [Customization Guide](#customization-guide)
11. [Troubleshooting](#troubleshooting)
12. [Deployment](#deployment)

---

## 🎯 Project Overview

This portfolio application is a full-stack Flask web application designed to showcase professional work, experiences, and technical skills. It features:

- **Public-facing portfolio website** with project showcase, blog, and experience sections
- **Admin control panel** for managing all content without database access
- **Dynamic content management** for projects, blog posts, experiences, and tools
- **Responsive design** for desktop, tablet, and mobile devices
- **File upload support** for project images and certificates
- **SEO-friendly** URLs and content structure
- **Authentication system** with admin login

---

## ✨ Features

### Public Features
- **Homepage** - Hero section with owner info, featured projects, experience, and tools
- **Projects Page** - Grid/list view of all projects with filtering and pagination
- **Project Details** - Individual project pages with image carousel, descriptions, and links
- **Blog Section** - Published blog posts linked to projects
- **About/Bio** - Customizable bio and contact information
- **Social Links** - Direct links to GitHub, LinkedIn, Twitter, email, etc.
- **Responsive Design** - Works perfectly on all devices

### Admin Features
- **Secure Login** - Protected admin panel with username/password authentication
- **Project Management**
  - Create/edit/delete projects
  - Multiple image uploads per project
  - Set project category (Web App, Mobile App, AI/ML, IoT/Embedded, Robotics, Hardware, Desktop App, Game Development, Data Science, Design, Other)
  - Add live demo and repository links
  - Track project timeline with start/end dates
  - Drag-and-drop image reordering

- **Blog Management**
  - Create/edit/delete blog posts
  - Auto-generated URL slugs
  - Link posts to projects
  - Publish/unpublish posts
  - Rich content support

- **Experience Management**
  - Add internships and work experience
  - Upload certificates for each experience
  - Track employment timeline
  - Add descriptions of role and achievements
  - Mark as ongoing
  - Order experiences for display

- **Tools & Technologies**
  - Manage programming languages and tools
  - Categorize tools (AI/ML, Web, DevOps, etc.)
  - Add proficiency levels
  - Set custom details/descriptions
  - Order by display priority

- **Site Settings**
  - Customize owner name and bio
  - Set hero text and site title
  - Add contact email
  - Link resume/CV
  - Manage social media links
  - Update site metadata

- **Dashboard**
  - Quick statistics (total projects, posts, images, experiences, tools)
  - Quick action buttons
  - System information

---

## 🛠️ Technology Stack

### Backend
- **Flask** (3.0.0) - Web framework
- **Flask-SQLAlchemy** (3.1.1) - ORM and database management
- **Flask-Login** (0.6.3) - User authentication
- **Werkzeug** (3.0.1) - WSGI utilities and security
- **Python-dotenv** (1.0.0) - Environment variable management

### Frontend
- **Bootstrap 5** - Responsive UI framework
- **HTML5** - Markup
- **CSS3** - Styling with custom variables
- **JavaScript (Vanilla)** - Interactivity (file uploads, drag-and-drop)

### Database
- **SQLite** (default) - Lightweight embedded database
  - Can be switched to PostgreSQL, MySQL, etc. via `DATABASE_URL`

### Security
- **Werkzeug Security** - Password hashing and validation
- **Flask-Login** - Session management
- **CSRF Protection** (can be added)

---

## 📁 Project Structure

```
portfolio-a/
├── app.py                      # Main Flask application with all routes
├── config.py                   # Configuration settings (Dev, Prod, Test)
├── models.py                   # SQLAlchemy database models
├── extensions.py               # Flask extensions initialization
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (gitignored)
├── .env.example                # Template for environment variables
├── .gitignore                  # Git ignore rules
├── portfolio.db                # SQLite database (auto-created)
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Main stylesheet (1000+ lines)
│   ├── js/
│   │   └── main.js            # JavaScript utilities
│   ├── uploads/               # User-uploaded images and certificates
│   │   └── [project images]
│   └── [other assets]
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html              # Base template with navbar and footer
│   ├── index.html             # Homepage with hero, projects, experience, tools
│   ├── projects.html          # Projects grid/list page
│   ├── project_detail.html    # Individual project page with carousel
│   ├── blog.html              # Blog posts listing
│   ├── post.html              # Individual blog post
│   ├── 404.html               # 404 error page
│   ├── 500.html               # 500 error page
│   │
│   └── admin/
│       ├── layout.html                 # Admin base layout with sidebar
│       ├── login.html                  # Admin login page
│       ├── dashboard.html              # Admin dashboard overview
│       ├── settings.html               # Site settings form
│       ├── projects_list.html          # Projects list (admin)
│       ├── project_form.html           # Project create/edit form
│       ├── experiences_list.html       # Experiences list (admin)
│       ├── experience_form.html        # Experience create/edit form
│       ├── tools_list.html             # Tools list (admin)
│       ├── tool_form.html              # Tool create/edit form
│       ├── posts_list.html             # Blog posts list (admin)
│       └── post_form.html              # Blog post create/edit form
│
├── instance/                   # Instance-specific files
│   └── [config overrides]
│
└── venv/                       # Virtual environment (gitignored)
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)

### Quick Setup (Recommended)

Use the provided setup scripts for automated environment creation and dependency installation:

**Windows (PowerShell):**
```powershell
.\setup.ps1
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

#### setup.ps1 (Windows)
```powershell
# Setup script for Windows - Creates virtual environment and installs dependencies

# Set execution policy for this process
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

Write-Host "Setting up Python virtual environment..." -ForegroundColor Green

# Check if venv already exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Virtual environment already exists" -ForegroundColor Yellow
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install requirements" -ForegroundColor Red
    exit 1
}

Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "Virtual environment is activated. You can now run the project." -ForegroundColor Cyan
```

---

### Manual Setup

### Step 1: Clone/Download Project
```bash
cd portfolio-a
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Create `.env` File

Copy `.env.example` to `.env` and customize:

```bash
# Copy example file
cp .env.example .env
```

Edit `.env` with your settings:
```env
# Flask Configuration
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-here-change-in-production

# Database
DATABASE_URL=sqlite:///portfolio.db

# Admin Credentials (default)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# File Upload
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216

# Session Settings
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
```

### Step 6: Run Application

**Using Run Script (Recommended):**

Windows (PowerShell):
```powershell
.\run.ps1
```

macOS/Linux:
```bash
chmod +x run.sh
./run.sh
```

#### run.ps1 (Windows)
```powershell
# Run script for Windows - Starts the Flask application

Write-Host "Starting Flask application..." -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Please run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Run the Flask app
Write-Host "Running Flask application on http://localhost:5000" -ForegroundColor Cyan
python app.py
```

**Manual Run:**
```bash
python app.py
```

The application will start at `http://127.0.0.1:5000`

### Step 7: First Login
- Navigate to `http://127.0.0.1:5000/admin/login`
- Username: `admin`
- Password: `admin123` (change in `.env`)

---

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `development` | Environment mode (development/production) |
| `SECRET_KEY` | `dev-secret-key-change-in-production` | Flask secret key for sessions |
| `DATABASE_URL` | `sqlite:///portfolio.db` | Database connection string |
| `ADMIN_USERNAME` | `admin` | Default admin username |
| `ADMIN_PASSWORD` | `admin123` | Default admin password |
| `UPLOAD_FOLDER` | `static/uploads` | Upload directory for images/certificates |
| `MAX_CONTENT_LENGTH` | `16777216` | Max file size (16MB) |
| `SESSION_COOKIE_SECURE` | `False` | HTTPS-only cookies (set True in production) |
| `SESSION_COOKIE_HTTPONLY` | `True` | Prevent JS from accessing cookies |
| `SESSION_COOKIE_SAMESITE` | `Lax` | CSRF protection level |
| `ITEMS_PER_PAGE` | `10` | Pagination items per page |

### Config Classes

**Development** (`config.py`)
- DEBUG = True
- TESTING = False
- Useful for development

**Production**
- DEBUG = False
- TESTING = False
- SESSION_COOKIE_SECURE = True (requires HTTPS)

**Testing**
- TESTING = True
- Uses in-memory SQLite database

---

## 📊 Database Models

### User
```python
- id (Integer, PK)
- username (String, Unique)
- password_hash (String)
```
Manages admin authentication.

### SiteSettings
```python
- id (Integer, PK)
- site_title (String)
- owner_name (String)
- bio (Text)
- hero_text (Text)
- contact_email (String)
- resume_url (String)
- social_links (JSON) - {platform: url, ...}
- created_at (DateTime)
- updated_at (DateTime)
```
Singleton model storing portfolio metadata.

### Project
```python
- id (Integer, PK)
- title (String, Required)
- description (Text)
- category (String)
- live_link (String) - URL to live demo
- repo_link (String) - URL to repository
- start_date (Date)
- end_date (Date)
- created_at (DateTime)
- updated_at (DateTime)
- Relationship: images (One-to-Many) ProjectImage
- Relationship: blog_posts (One-to-Many) BlogPost
```
Represents portfolio projects.

### ProjectImage
```python
- id (Integer, PK)
- project_id (Integer, FK)
- image_path (String) - /static/uploads/...
- alt_text (String)
- order (Integer) - Display order
- created_at (DateTime)
```
Stores multiple images per project.

### BlogPost
```python
- id (Integer, PK)
- title (String, Required)
- slug (String, Unique) - URL-friendly
- content (Text)
- project_id (Integer, FK, Optional)
- published (Boolean)
- created_at (DateTime)
- updated_at (DateTime)
```
Blog articles, optionally linked to projects.

### Experience
```python
- id (Integer, PK)
- title (String, Required)
- company (String)
- location (String)
- role (String)
- start_date (Date)
- end_date (Date)
- ongoing (Boolean)
- description (Text)
- certificate_image_path (String) - /static/uploads/...
- order (Integer) - Display order
- created_at (DateTime)
```
Work/internship experiences with optional certificate upload.

### Tool
```python
- id (Integer, PK)
- name (String, Required)
- category (String)
- details (Text)
- proficiency (String) - Basic/Intermediate/Advanced
- order (Integer) - Display order
- created_at (DateTime)
```
Programming languages and tools used.

---

## 🔐 Admin Panel Guide

### Accessing Admin Panel
1. Go to `http://your-site.com/admin/login`
2. Enter credentials (default: admin/admin123)
3. Access dashboard at `http://your-site.com/admin`

### Admin Dashboard
- Quick stats showing:
  - Total Projects
  - Total Blog Posts
  - Total Images
  - Total Experiences
  - Total Tools
- Quick action buttons to create new content

### Managing Site Settings
1. Click **Settings** in sidebar
2. Update:
   - Site title
   - Owner name
   - Bio/About text
   - Hero text (tagline)
   - Contact email
   - Social media links
3. Click **Save Settings**

### Managing Projects
1. Click **Projects** in sidebar
2. Click **➕ New Project** to create
3. Fill in:
   - Project title (required)
   - Category (select or custom)
   - Start/end dates
   - Description (HTML supported)
   - Live demo URL
   - Repository URL
   - Upload project images (drag-and-drop supported)
4. Click **💾 Create Project**
5. Edit: Click **✏️ Edit** button
6. Delete: Click **🗑️ Delete** button (confirmation required)

#### Category Options
- 🌐 Web App
- 📱 Mobile App
- 💻 Desktop App
- ⚙️ Backend
- 🤖 AI/ML
- 📊 Data Science
- 📡 IoT/Embedded
- 🔧 Hardware
- 🦾 Robotics
- 🎮 Game Development
- 🎨 Design
- 📦 Other

### Managing Blog Posts
1. Click **Blog Posts** in sidebar
2. Click **➕ New Blog Post** to create
3. Fill in:
   - Post title (required)
   - Content/article body
   - Link to related project (optional)
   - Published status (toggle)
4. Click **💾 Create Post**
5. URL slug auto-generated from title
6. Edit/Delete similar to projects

### Managing Experience
1. Click **💼 Experiences** in sidebar
2. Click **➕ New Experience** to create
3. Fill in:
   - Experience title (required)
   - Company name
   - Role/position
   - Location
   - Start date
   - End date
   - Check "Currently Working" if ongoing
   - Description (achievements, responsibilities)
   - Upload certificate image (optional)
   - Set display order
4. Click **Save**

### Managing Tools
1. Click **🛠️ Tools** in sidebar
2. Click **➕ New Tool** to create
3. Fill in:
   - Tool name (required)
   - Category (e.g., AI/ML, Web, DevOps)
   - Proficiency (Basic, Intermediate, Advanced)
   - Details/description
   - Set display order
4. Click **Save**

---

## 🌐 Public Pages & Routes

### Public Routes

| Route | Template | Description |
|-------|----------|-------------|
| `/` | `index.html` | Homepage with hero, projects, experience, tools |
| `/projects` | `projects.html` | All projects with pagination |
| `/project/<id>` | `project_detail.html` | Individual project with full details |
| `/blog` | `blog.html` | All published blog posts |
| `/blog/<slug>` | `post.html` | Individual blog post |
| `/404` | `404.html` | Not found page |
| `/500` | `500.html` | Server error page |

### Admin Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/admin/login` | GET, POST | Admin login |
| `/admin/logout` | GET | Admin logout |
| `/admin` `/admin/dashboard` | GET | Dashboard overview |
| `/admin/settings` | GET, POST | Update site settings |
| `/admin/projects` | GET | List all projects |
| `/admin/project/new` | GET, POST | Create project |
| `/admin/project/<id>/edit` | GET, POST | Edit project |
| `/admin/project/<id>/delete` | POST | Delete project |
| `/admin/project/<id>/image/<img_id>/delete` | POST | Delete project image |
| `/admin/experiences` | GET | List experiences |
| `/admin/experience/new` | GET, POST | Create experience |
| `/admin/experience/<id>/edit` | GET, POST | Edit experience |
| `/admin/experience/<id>/delete` | POST | Delete experience |
| `/admin/tools` | GET | List tools |
| `/admin/tool/new` | GET, POST | Create tool |
| `/admin/tool/<id>/edit` | GET, POST | Edit tool |
| `/admin/tool/<id>/delete` | POST | Delete tool |
| `/admin/posts` | GET | List blog posts |
| `/admin/post/new` | GET, POST | Create post |
| `/admin/post/<id>/edit` | GET, POST | Edit post |
| `/admin/post/<id>/delete` | POST | Delete post |

---

## 🎨 Customization Guide

### Changing Colors

#### Hero Section Background
Edit `static/css/style.css`, line ~168:
```css
.hero {
    background: linear-gradient(135deg, var(--dark-bg) 0%, #1a2d5e 100%);
}
```

#### Bio/About Text Color
Edit `static/css/style.css`, line ~512:
```css
.text-muted { 
    color: var(--text-light) !important; 
}
```
Change `var(--text-light)` to any color (e.g., `#FFFFFF`, `var(--primary-light)`).

#### Color Variables
Available in `static/css/style.css` `:root`:
```css
--primary-color: #5B4CF5;      /* Purple */
--primary-light: #8B7FFF;      /* Light purple */
--primary-dark: #4438D1;       /* Dark purple */
--success-color: #10B981;      /* Green */
--warning-color: #F59E0B;      /* Orange */
--danger-color: #EF4444;       /* Red */
--white: #FFFFFF;              /* White */
--text-light: #64748B;         /* Light gray */
--dark-bg: #5d6881;            /* Dark background */
```

### Adding New Project Categories

Edit `templates/admin/project_form.html`, line ~37-48:
```html
<select class="form-control form-control-lg" name="category" id="category">
    <option value="">Select a category</option>
    <option value="Your Category">📦 Your Category</option>
    <!-- Add more options here -->
</select>
```

### Modifying Homepage Sections

Edit `templates/index.html`:
- **Hero Section**: Lines 7-27
- **Featured Projects**: Lines 30-75
- **Experience & Tools**: Lines 78-132
- **Contact Section**: Lines 135-180

### Customizing Fonts

Edit `static/css/style.css` `:root`:
```css
--font-sans: 'Sora', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'Space Mono', monospace;
```

### Adding New Pages

1. Create template in `templates/your_page.html`
2. Extend `base.html`:
   ```html
   {% extends "base.html" %}
   {% block content %}
   <!-- Your content -->
   {% endblock %}
   ```
3. Add route in `app.py`:
   ```python
   @app.route('/your-page')
   def your_page():
       return render_template('your_page.html')
   ```
4. Add navigation link in `templates/base.html`

---

## 🐛 Troubleshooting

### Issue: Database Column Missing Error
**Error:** `no such column: experience.certificate_image_path`

**Solution:**
The app includes automatic migration. Restart the server:
```bash
python app.py
```

If still failing, delete `portfolio.db` and restart (will recreate with all tables).

### Issue: Admin Login Not Working
**Solution:**
1. Check `.env` file has correct `ADMIN_USERNAME` and `ADMIN_PASSWORD`
2. Delete `portfolio.db` to reset admin user
3. Restart server

### Issue: File Uploads Not Working
**Solution:**
1. Check `static/uploads/` folder exists
2. Verify file permissions (should be writable)
3. Check `MAX_CONTENT_LENGTH` in `.env` (16MB default)
4. Supported formats: PNG, JPG, JPEG, GIF, WebP

### Issue: Images Not Displaying
**Solution:**
1. Check image paths in database
2. Verify images exist in `static/uploads/`
3. Check CSS for image styling issues
4. Use browser DevTools to check image URL

### Issue: Admin Panel Styles Not Loading
**Solution:**
1. Hard refresh browser (Ctrl+Shift+R on Windows/Linux, Cmd+Shift+R on Mac)
2. Clear browser cache
3. Check `static/css/style.css` exists

### Issue: Port Already in Use
**Error:** `Address already in use`

**Solution:**
```bash
# On Windows
netstat -ano | findstr :5000
taskkill /PID [PID] /F

# On macOS/Linux
lsof -ti:5000 | xargs kill -9
```

---

## 📦 Deployment

### Deployment Checklist

#### Security
- [ ] Change `SECRET_KEY` in `.env`
- [ ] Change admin credentials in `.env`
- [ ] Set `SESSION_COOKIE_SECURE=True` in `.env`
- [ ] Set `FLASK_ENV=production`
- [ ] Disable debug mode

#### Database
- [ ] Switch to PostgreSQL/MySQL for production
- [ ] Backup database before deploying
- [ ] Set `DATABASE_URL` connection string

#### Files
- [ ] Ensure `static/uploads/` directory exists with write permissions
- [ ] Backup uploaded images regularly

### Deployment Platforms

#### Heroku
```bash
# Install Heroku CLI
heroku create your-portfolio-name
git push heroku main
```

Create `Procfile`:
```
web: gunicorn app:create_app()
```

Add dependencies:
```bash
pip install gunicorn
```

#### PythonAnywhere
1. Upload code via Git
2. Create virtual environment
3. Set up WSGI configuration
4. Configure custom domain

#### DigitalOcean/AWS/Azure
1. Create server instance
2. Install Python 3.8+
3. Clone repository
4. Install dependencies
5. Configure reverse proxy (Nginx)
6. Use production WSGI server (Gunicorn, uWSGI)

### Production WSGI Server

Replace Flask development server with Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app()'
```

---

## 📝 Usage Examples

### Adding Your First Project
1. Log in to admin panel
2. Go to Projects → New Project
3. Add title: "E-commerce Platform"
4. Category: Web App
5. Description: `<strong>Built with:</strong> Python, Flask, PostgreSQL...`
6. Upload 3-5 project images
7. Add live demo and GitHub links
8. Set start/end dates
9. Save and view on homepage

### Adding Experience
1. Go to Experiences → New Experience
2. Add title: "AI/ML Intern"
3. Company: "99Ideas SaaS"
4. Role: "Machine Learning Engineer"
5. Description: "Developed Q&A systems using Transformers..."
6. Upload certificate
7. Mark as "Currently Working" if applicable
8. Save and view on homepage

### Writing Blog Post
1. Go to Blog Posts → New Blog Post
2. Title: "Building a Q&A System with LLMs"
3. Content: Full article in Markdown or HTML
4. Link to related project
5. Publish and it appears in blog section

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks
- Backup database weekly
- Backup uploaded images monthly
- Update dependencies quarterly
- Review and delete old drafts
- Monitor server logs

### Troubleshooting Resources
- Check `app.py` for route implementations
- Review `models.py` for data structure
- Check `config.py` for configuration options
- Use browser DevTools (F12) for frontend issues
- Check terminal/console for Flask errors

---

## 📄 License

This project is open-source and available for personal and commercial use.

---

## 👤 Author

**Aditya Choudhary**
- AI/ML Enthusiast
- Backend Developer
- Computer Science Engineering Student

---

## 🙏 Acknowledgments

- Built with **Flask** and **Bootstrap 5**
- Database powered by **SQLAlchemy**
- Icons and emojis for better UX

---

**Last Updated:** January 17, 2026  
**Portfolio Status:** ✅ Production Ready
