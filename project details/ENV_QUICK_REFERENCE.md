# Environment Variables Quick Reference

## What Changed?

Admin credentials and configuration are now loaded from `.env` file instead of being hardcoded.

## Files You Need to Know

| File | Purpose | Git Tracked |
|------|---------|------------|
| `.env` | Your local/server credentials | ❌ No (in .gitignore) |
| `.env.example` | Template for reference | ✅ Yes |
| `.gitignore` | Excludes .env from git | ✅ Yes |
| `config.py` | Reads from environment | ✅ Yes |
| `app.py` | Uses admin credentials from env | ✅ Yes |

## Default Credentials (Development)

Located in `.env`:
```
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

## Quick Setup

### For Development
1. `.env` file already created ✅
2. Just run: `python app.py`
3. Login with `admin` / `admin123`

### For Production
1. Set environment variables on your server
2. Examples:
   ```bash
   # Heroku
   heroku config:set ADMIN_USERNAME=myuser
   heroku config:set ADMIN_PASSWORD=mypass
   
   # Docker
   docker run -e ADMIN_USERNAME=user -e ADMIN_PASSWORD=pass myapp
   
   # Linux/Mac server
   export ADMIN_USERNAME=user
   export ADMIN_PASSWORD=pass
   python app.py
   ```

## All Environment Variables

### Required (but have defaults)
- `ADMIN_USERNAME` → Login username
- `ADMIN_PASSWORD` → Login password
- `SECRET_KEY` → Session encryption

### Optional (Flask)
- `FLASK_ENV` → Mode (development/production)
- `FLASK_DEBUG` → Enable debugger (True/False)

### Optional (Database)
- `DATABASE_URL` → Database connection string

### Optional (Session Security)
- `SESSION_COOKIE_SECURE` → HTTPS only (False for dev, True for prod)
- `SESSION_COOKIE_HTTPONLY` → Prevent JS access (True)
- `SESSION_COOKIE_SAMESITE` → CSRF protection (Lax)

### Optional (Upload)
- `MAX_CONTENT_LENGTH` → Max file size in bytes
- `UPLOAD_FOLDER` → Where to save uploads

### Optional (Pagination)
- `ITEMS_PER_PAGE` → Items per page

## Generate Secure Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy output and set `SECRET_KEY` in `.env`

## How python-dotenv Works

```
.env file with KEY=VALUE
        ↓
python-dotenv reads it
        ↓
Sets environment variables
        ↓
os.getenv('KEY') retrieves value
        ↓
Default value used if not set
```

## Important Security Rules

✅ **DO THIS:**
- Change credentials before production
- Use strong passwords
- Keep `.env` file safe
- Use `.env.example` as template

❌ **DON'T DO THIS:**
- Commit `.env` to git
- Share `.env` file
- Use weak passwords
- Hardcode credentials in Python

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Admin login fails | Check credentials in `.env` |
| Config not loading | Restart app after changing `.env` |
| Can't find `.env` | Must be in project root folder |
| Wrong environment | Verify `FLASK_ENV` in `.env` |

## Common `.env` Configs

### Development
```env
FLASK_ENV=development
FLASK_DEBUG=True
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
SECRET_KEY=dev-key
SESSION_COOKIE_SECURE=False
DATABASE_URL=sqlite:///portfolio.db
```

### Production
```env
FLASK_ENV=production
FLASK_DEBUG=False
ADMIN_USERNAME=your-username
ADMIN_PASSWORD=strong-password
SECRET_KEY=strong-random-key
SESSION_COOKIE_SECURE=True
DATABASE_URL=postgresql://user:pass@host/db
```

## File Locations

```
portfolio-a/
├── .env                          ← Your credentials (NOT in git)
├── .env.example                  ← Template (in git)
├── .gitignore                    ← Excludes .env (in git)
├── config.py                     ← Reads from environment (in git)
├── app.py                        ← Uses environment (in git)
├── requirements.txt              ← Includes python-dotenv (in git)
└── ...
```

## What Gets Loaded Where

```python
# config.py
SECRET_KEY = os.getenv('SECRET_KEY', 'default')
        ↓
# Checks .env, uses default if not found

# app.py
admin_username = os.getenv('ADMIN_USERNAME', 'admin')
admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        ↓
# Creates admin user with these credentials
```

## Before vs After

### Before (Hardcoded)
```python
# app.py
admin = User(username='admin')
admin.set_password('admin123')
```
❌ Credentials in code
❌ Same everywhere
❌ Not secure

### After (Environment)
```python
# .env
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# app.py
username = os.getenv('ADMIN_USERNAME', 'admin')
password = os.getenv('ADMIN_PASSWORD', 'admin123')
admin = User(username=username)
admin.set_password(password)
```
✅ Credentials in .env
✅ Different per environment
✅ Much more secure

## Support

- Full guide: `ENV_CONFIGURATION_GUIDE.md`
- Implementation details: `ENV_IMPLEMENTATION_SUMMARY.md`
- Template: `.env.example`

Questions? Check the full documentation files above!
