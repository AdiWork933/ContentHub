from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """Admin User Model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class SiteSettings(db.Model):
    """Site Settings - Singleton for portfolio metadata"""
    id = db.Column(db.Integer, primary_key=True)
    site_title = db.Column(db.String(255), default="My Portfolio")
    owner_name = db.Column(db.String(255), default="Developer")
    bio = db.Column(db.Text, default="Welcome to my portfolio")
    hero_text = db.Column(db.Text, default="Full Stack Developer")
    contact_email = db.Column(db.String(255))
    resume_url = db.Column(db.String(255))
    social_links = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def get_settings():
        """Get or create singleton settings"""
        settings = SiteSettings.query.first()
        if not settings:
            settings = SiteSettings()
            db.session.add(settings)
            db.session.commit()
        return settings


class Project(db.Model):
    """Project Model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    live_link = db.Column(db.String(255))
    repo_link = db.Column(db.String(255))
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    images = db.relationship('ProjectImage', backref='project', lazy=True, cascade='all, delete-orphan')
    blog_posts = db.relationship('BlogPost', backref='related_project', lazy=True)


class ProjectImage(db.Model):
    """Project Image Model - One-to-Many relationship with Project"""
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    alt_text = db.Column(db.String(255))
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class BlogPost(db.Model):
    """Blog Post Model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True)
    content = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def generate_slug(self):
        """Generate URL-friendly slug from title"""
        import re
        slug = self.title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')


class Experience(db.Model):
    """Work / Internship Experience"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    company = db.Column(db.String(255))
    location = db.Column(db.String(255))
    role = db.Column(db.String(255))
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    ongoing = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    certificate_image_path = db.Column(db.String(255))
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Tool(db.Model):
    """Tools / Technologies used"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255))
    details = db.Column(db.Text)
    proficiency = db.Column(db.String(64))
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
