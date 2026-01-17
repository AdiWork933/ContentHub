# Environment Configuration Guide

## Overview

All sensitive credentials and configuration settings have been moved from hardcoded values into a `.env` file using `python-dotenv`. This ensures better security and easier deployment across different environments.

## What Changed

### Before
Credentials were hardcoded directly in the application code:
```python
# app.py (BEFORE)
admin = User(username='admin')
admin.set_password('admin123')
```

### After
Credentials are loaded from environment variables:
```python
# app.py (AFTER)
admin_username = os.getenv('ADMIN_USERNAME', 'admin')
admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
admin = User(username=admin_username)
admin.set_password(admin_password)
```

## Files Added/Modified

### New Files
- **`.env`** - Development environment variables (not tracked in git)
- **`.env.example`** - Template showing all available environment variables
- **`.gitignore`** - Updated to exclude `.env` file from version control

### Modified Files
- **`requirements.txt`** - Added `python-dotenv==1.0.0` dependency
- **`config.py`** - Updated to load all settings from environment variables
- **`app.py`** - Updated to read admin credentials from `.env`

## Environment Variables

### Admin Credentials
```env
# Admin user credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### Flask Configuration
```env
# Flask environment and debugging
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=portfolio-dev-secret-key-2024-change-in-production
```

### Database Configuration
```env
# Database URL
DATABASE_URL=sqlite:///portfolio.db
```

### Session Settings
```env
# Session cookie security settings
SESSION_COOKIE_SECURE=False      # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
```

### Upload Settings
```env
# File upload configuration
MAX_CONTENT_LENGTH=16777216      # 16MB in bytes
UPLOAD_FOLDER=static/uploads
```

### Pagination
```env
# Number of items per page
ITEMS_PER_PAGE=10
```

## Setup Instructions

### 1. First Time Setup

```bash
# Install dependencies including python-dotenv
pip install -r requirements.txt
```

### 2. Create .env File

The `.env` file is already created with default development credentials. Copy from `.env.example` if needed:

```bash
# On Windows PowerShell
Copy-Item .env.example .env

# On Linux/Mac
cp .env.example .env
```

### 3. (Optional) Customize for Your Environment

Edit `.env` file to change default values:

```env
ADMIN_USERNAME=your-username
ADMIN_PASSWORD=your-secure-password
SECRET_KEY=your-random-secret-key
```

Generate a secure secret key:
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4. Run the Application

```bash
python app.py
```

The admin user will be created automatically on first run with credentials from `.env`.

## Environment-Specific Configuration

### Development
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=any-dev-key-is-fine
SESSION_COOKIE_SECURE=False
```

### Production
```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=use-a-strong-random-key
SESSION_COOKIE_SECURE=True
DATABASE_URL=postgresql://user:password@host/dbname
```

### Testing
```env
FLASK_ENV=testing
FLASK_DEBUG=False
DATABASE_URL=sqlite:///:memory:
```

## Security Best Practices

### ✅ Do's
- Change `ADMIN_PASSWORD` to a strong, unique password
- Use environment variables for all sensitive data
- Keep `.env` file out of version control (it's in `.gitignore`)
- Regenerate `SECRET_KEY` for production
- Use strong `SECRET_KEY` with at least 32 characters
- Set `SESSION_COOKIE_SECURE=True` in production with HTTPS
- Use `DATABASE_URL` with strong credentials in production

### ❌ Don'ts
- Don't commit `.env` file to git repository
- Don't use default passwords in production
- Don't share `.env` file via email or chat
- Don't hardcode credentials in Python files
- Don't set `SECRET_KEY` to a weak value
- Don't disable security cookies in production
- Don't use SQLite in production for high-traffic sites

## Deployment

### Heroku
```bash
# Set environment variables via Heroku CLI
heroku config:set ADMIN_USERNAME=your-username
heroku config:set ADMIN_PASSWORD=your-password
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
heroku config:set FLASK_ENV=production
```

### Docker
```dockerfile
FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Set environment variables
ENV FLASK_ENV=production
ENV ADMIN_USERNAME=${ADMIN_USERNAME}
ENV ADMIN_PASSWORD=${ADMIN_PASSWORD}
ENV SECRET_KEY=${SECRET_KEY}

CMD ["python", "app.py"]
```

Then run with:
```bash
docker run -e ADMIN_USERNAME=admin -e ADMIN_PASSWORD=secure_password myapp
```

### AWS, Azure, Google Cloud
Use their respective secrets management services:
- AWS: Secrets Manager or Parameter Store
- Azure: Key Vault
- Google Cloud: Secret Manager

Set environment variables from these services before starting the application.

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'dotenv'"
**Solution:**
```bash
pip install python-dotenv
```

### Issue: Admin user not found after restarting
**Solution:**
1. Ensure `.env` file exists in project root
2. Check `ADMIN_USERNAME` and `ADMIN_PASSWORD` in `.env`
3. Delete `instance/portfolio.db` to reset database
4. Restart application

### Issue: Cannot connect to database
**Solution:**
1. Check `DATABASE_URL` in `.env`
2. Ensure database file/server is accessible
3. Verify path permissions for SQLite

### Issue: Session cookies not working
**Solution:**
1. Verify `SESSION_COOKIE_SECURE` matches your setup (False for HTTP, True for HTTPS)
2. Check `SESSION_COOKIE_HTTPONLY` is True
3. Verify `SESSION_COOKIE_SAMESITE` is set correctly

## Configuration Reference

| Variable | Type | Default | Purpose |
|----------|------|---------|---------|
| `FLASK_ENV` | string | development | Flask environment mode |
| `FLASK_DEBUG` | boolean | True | Enable Flask debugger |
| `SECRET_KEY` | string | random | Session encryption key |
| `ADMIN_USERNAME` | string | admin | Admin login username |
| `ADMIN_PASSWORD` | string | admin123 | Admin login password |
| `DATABASE_URL` | string | sqlite:///portfolio.db | Database connection |
| `SESSION_COOKIE_SECURE` | boolean | False | Require HTTPS for cookies |
| `SESSION_COOKIE_HTTPONLY` | boolean | True | Prevent JS cookie access |
| `SESSION_COOKIE_SAMESITE` | string | Lax | CSRF protection level |
| `MAX_CONTENT_LENGTH` | integer | 16777216 | Max upload size (bytes) |
| `UPLOAD_FOLDER` | string | static/uploads | Upload directory |
| `ITEMS_PER_PAGE` | integer | 10 | Pagination size |

## How dotenv Works

The `python-dotenv` package:
1. Reads the `.env` file from the project root
2. Loads all `KEY=VALUE` pairs into `os.environ`
3. Allows access via `os.getenv('KEY', 'default')`
4. Automatically loads on application startup

Example workflow:
```python
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access variables
username = os.getenv('ADMIN_USERNAME', 'admin')
password = os.getenv('ADMIN_PASSWORD', 'admin123')
```

## Version Control

### .env File
- **Should NOT be committed** to version control
- Contains sensitive credentials
- Automatically excluded via `.gitignore`
- Each developer/environment has their own copy

### .env.example File
- **Should be committed** to version control
- Shows all available configuration options
- Contains safe default values or placeholder text
- Helps new developers understand required setup

## Migration from Old Setup

If upgrading from hardcoded credentials:

1. Update all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. Customize `.env` with your settings

4. Delete old database to trigger re-initialization:
   ```bash
   rm instance/portfolio.db
   ```

5. Start the application:
   ```bash
   python app.py
   ```

## FAQ

### Q: Why use .env instead of environment variables?
**A:** `.env` files are convenient for development. In production, set actual environment variables through your hosting platform.

### Q: Can I use different .env files for different environments?
**A:** Yes, you can:
```python
load_dotenv('.env.production')  # Load specific file
```

Or name them `.env.development`, `.env.production`, etc.

### Q: What if I forget to set a variable?
**A:** All variables have defaults in the code, so the app will still run. However, use the defaults provided in `.env.example` for security.

### Q: How do I generate a strong SECRET_KEY?
**A:** Use Python:
```python
import secrets
print(secrets.token_hex(32))
```

Or use online generators, but never share the key.

### Q: Is .env exposed if I deploy to a web server?
**A:** No, if properly configured:
- `.gitignore` prevents git commits
- Web servers don't serve `.env` files
- Set environment variables via hosting platform instead

### Q: Can multiple developers use the same .env?
**A:** Not recommended. Each developer should have their own `.env` with personal credentials for security.

## Next Steps

1. ✅ Review all environment variables
2. ✅ Customize credentials in `.env`
3. ✅ Regenerate `SECRET_KEY` for production
4. ✅ Test admin login with new credentials
5. ✅ Update deployment scripts with environment setup
6. ✅ Document any additional environment variables your project needs

## Support

For issues or questions:
1. Check `.env.example` for all available variables
2. Review the configuration reference table above
3. Verify environment variables are properly set
4. Check application logs for error messages
5. Restart the application after changing `.env` values
