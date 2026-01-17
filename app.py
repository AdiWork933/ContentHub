from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime, date
from functools import wraps
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from extensions import db, login_manager
from config import config_by_name
from models import User, SiteSettings, Project, ProjectImage, BlogPost, Experience, Tool


def create_app(config_name='development'):
    """Application Factory"""
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin_login'
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    @app.before_request
    def before_request():
        """Initialize database and create tables if needed"""
        with app.app_context():
            db.create_all()
            # Ensure admin user exists
            if not db.session.query(User).first():
                admin_username = os.getenv('ADMIN_USERNAME', 'admin')
                admin_password = os.getenv('ADMIN_PASSWORD', 'admin123')
                admin = User(username=admin_username)
                admin.set_password(admin_password)
                db.session.add(admin)
                db.session.commit()
            # Ensure settings exist
            SiteSettings.get_settings()
            # -- Lightweight schema migration for added fields (SQLite)
            try:
                # Check if certificate_image_path column exists in experience table
                inspector = db.inspect(db.engine)
                cols = [c['name'] for c in inspector.get_columns('experience')]
                if 'certificate_image_path' not in cols:
                    # SQLite supports ADD COLUMN
                    db.engine.execute('ALTER TABLE experience ADD COLUMN certificate_image_path VARCHAR(255)')
            except Exception:
                # If any error occurs, skip migration (table may not exist yet)
                pass
    
    def allowed_file(filename):
        """Check if file is allowed"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    
    def admin_required(f):
        """Decorator to require admin login"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('admin_login'))
            return f(*args, **kwargs)
        return decorated_function
    
    # ===================== PUBLIC ROUTES =====================
    
    @app.route('/')
    def index():
        """Homepage"""
        from datetime import datetime
        settings = SiteSettings.get_settings()
        featured_projects = Project.query.limit(6).all()
        experiences = Experience.query.order_by(Experience.order.asc(), Experience.start_date.desc().nulls_last()).all()
        tools = Tool.query.order_by(Tool.order.asc(), Tool.name.asc()).all()
        return render_template('index.html', settings=settings, projects=featured_projects, experiences=experiences, tools=tools, current_year=datetime.now().year)
    
    @app.route('/projects')
    def projects():
        """Projects Grid View"""
        page = request.args.get('page', 1, type=int)
        projects = Project.query.paginate(page=page, per_page=12)
        return render_template('projects.html', projects=projects)
    
    @app.route('/project/<int:project_id>')
    def project_detail(project_id):
        """Single Project Detail with Image Carousel"""
        project = Project.query.get_or_404(project_id)
        return render_template('project_detail.html', project=project)
    
    @app.route('/blog')
    def blog():
        """Blog Feed"""
        page = request.args.get('page', 1, type=int)
        posts = BlogPost.query.filter_by(published=True).order_by(
            BlogPost.created_at.desc()
        ).paginate(page=page, per_page=10)
        return render_template('blog.html', posts=posts)
    
    @app.route('/blog/<slug>')
    def blog_post(slug):
        """Single Blog Post"""
        post = BlogPost.query.filter_by(slug=slug).first_or_404()
        return render_template('post.html', post=post)
    
    # ===================== ADMIN ROUTES =====================
    
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        """Admin Login"""
        if current_user.is_authenticated:
            return redirect(url_for('admin_dashboard'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user, remember=request.form.get('remember'))
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password.', 'danger')
        
        return render_template('admin/login.html')
    
    @app.route('/admin/logout')
    @login_required
    def admin_logout():
        """Admin Logout"""
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('index'))
    
    @app.route('/admin')
    @app.route('/admin/dashboard')
    @admin_required
    def admin_dashboard():
        """Admin Dashboard Overview"""
        total_projects = Project.query.count()
        total_posts = BlogPost.query.count()
        total_images = ProjectImage.query.count()
        total_experiences = Experience.query.count()
        total_tools = Tool.query.count()
        
        context = {
            'total_projects': total_projects,
            'total_posts': total_posts,
            'total_images': total_images,
            'total_experiences': total_experiences,
            'total_tools': total_tools,
        }
        return render_template('admin/dashboard.html', **context)
    
    # ================= SETTINGS MANAGEMENT =================
    
    @app.route('/admin/settings', methods=['GET', 'POST'])
    @admin_required
    def admin_settings():
        """Manage Site Settings"""
        settings = SiteSettings.get_settings()
        
        if request.method == 'POST':
            settings.site_title = request.form.get('site_title')
            settings.owner_name = request.form.get('owner_name')
            settings.hero_text = request.form.get('hero_text')
            settings.bio = request.form.get('bio')
            settings.contact_email = request.form.get('contact_email')
            
            # Handle social links
            social_links = {}
            for platform in ['github', 'linkedin', 'twitter', 'email']:
                value = request.form.get(f'social_{platform}')
                if value:
                    social_links[platform] = value
            settings.social_links = social_links
            
            db.session.commit()
            flash('Settings updated successfully!', 'success')
            return redirect(url_for('admin_settings'))
        
        return render_template('admin/settings.html', settings=settings)
    
    # ================= PROJECT MANAGEMENT =================
    
    @app.route('/admin/projects')
    @admin_required
    def admin_projects():
        """List all projects"""
        page = request.args.get('page', 1, type=int)
        projects = Project.query.order_by(Project.created_at.desc()).paginate(
            page=page, per_page=10
        )
        return render_template('admin/projects_list.html', projects=projects)

    # ================= EXPERIENCE MANAGEMENT =================

    @app.route('/admin/experiences')
    @admin_required
    def admin_experiences():
        page = request.args.get('page', 1, type=int)
        experiences = Experience.query.order_by(Experience.start_date.desc().nulls_last()).paginate(page=page, per_page=10)
        return render_template('admin/experiences_list.html', experiences=experiences)

    @app.route('/admin/experience/new', methods=['GET', 'POST'])
    @app.route('/admin/experience/<int:experience_id>/edit', methods=['GET', 'POST'])
    @admin_required
    def admin_experience_form(experience_id=None):
        experience = None
        if experience_id:
            experience = Experience.query.get_or_404(experience_id)

        if request.method == 'POST':
            if not experience:
                experience = Experience()

            experience.title = request.form.get('title')
            experience.company = request.form.get('company')
            experience.location = request.form.get('location')
            experience.role = request.form.get('role')
            experience.description = request.form.get('description')
            experience.order = int(request.form.get('order') or 0)

            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')
            experience.ongoing = request.form.get('ongoing') == 'on'

            if start_date_str:
                experience.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            else:
                experience.start_date = None

            if end_date_str:
                experience.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            else:
                experience.end_date = None

            if not experience.id:
                db.session.add(experience)
            # Handle certificate upload
            certificate = request.files.get('certificate')
            if certificate and allowed_file(certificate.filename):
                filename = secure_filename(certificate.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                filename = timestamp + filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                certificate.save(filepath)
                experience.certificate_image_path = f'/static/uploads/{filename}'

            db.session.commit()
            flash(f'Experience {"created" if not experience_id else "updated"} successfully!', 'success')
            return redirect(url_for('admin_experiences'))

        return render_template('admin/experience_form.html', experience=experience)

    @app.route('/admin/experience/<int:experience_id>/delete', methods=['POST'])
    @admin_required
    def admin_experience_delete(experience_id):
        experience = Experience.query.get_or_404(experience_id)
        # Delete certificate file from filesystem if present
        if experience.certificate_image_path:
            image_path = experience.certificate_image_path.lstrip('/')
            filepath = os.path.join(app.root_path, image_path)
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception:
                pass

        db.session.delete(experience)
        db.session.commit()
        flash('Experience deleted successfully!', 'success')
        return redirect(url_for('admin_experiences'))

    # ================= TOOL MANAGEMENT =================

    @app.route('/admin/tools')
    @admin_required
    def admin_tools():
        page = request.args.get('page', 1, type=int)
        tools = Tool.query.order_by(Tool.order.asc(), Tool.name.asc()).paginate(page=page, per_page=20)
        return render_template('admin/tools_list.html', tools=tools)

    @app.route('/admin/tool/new', methods=['GET', 'POST'])
    @app.route('/admin/tool/<int:tool_id>/edit', methods=['GET', 'POST'])
    @admin_required
    def admin_tool_form(tool_id=None):
        tool = None
        if tool_id:
            tool = Tool.query.get_or_404(tool_id)

        if request.method == 'POST':
            if not tool:
                tool = Tool()

            tool.name = request.form.get('name')
            tool.category = request.form.get('category')
            tool.details = request.form.get('details')
            tool.proficiency = request.form.get('proficiency')
            tool.order = int(request.form.get('order') or 0)

            if not tool.id:
                db.session.add(tool)
            db.session.commit()
            flash(f'Tool {"created" if not tool_id else "updated"} successfully!', 'success')
            return redirect(url_for('admin_tools'))

        return render_template('admin/tool_form.html', tool=tool)

    @app.route('/admin/tool/<int:tool_id>/delete', methods=['POST'])
    @admin_required
    def admin_tool_delete(tool_id):
        tool = Tool.query.get_or_404(tool_id)
        db.session.delete(tool)
        db.session.commit()
        flash('Tool deleted successfully!', 'success')
        return redirect(url_for('admin_tools'))
    
    @app.route('/admin/project/new', methods=['GET', 'POST'])
    @app.route('/admin/project/<int:project_id>/edit', methods=['GET', 'POST'])
    @admin_required
    def admin_project_form(project_id=None):
        """Create or Edit Project"""
        project = None
        if project_id:
            project = Project.query.get_or_404(project_id)
        
        if request.method == 'POST':
            if not project:
                project = Project()
            
            project.title = request.form.get('title')
            project.description = request.form.get('description')
            project.category = request.form.get('category')
            project.live_link = request.form.get('live_link')
            project.repo_link = request.form.get('repo_link')
            
            # Handle date fields
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')
            
            if start_date_str:
                project.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            if end_date_str:
                project.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            if not project.id:
                db.session.add(project)
                db.session.flush()
            
            # Handle multiple image uploads
            uploaded_files = request.files.getlist('images')
            for idx, file in enumerate(uploaded_files):
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                    filename = timestamp + filename
                    
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    
                    image = ProjectImage(
                        project_id=project.id,
                        image_path=f'/static/uploads/{filename}',
                        order=idx
                    )
                    db.session.add(image)
            
            db.session.commit()
            flash(f'Project {"created" if not project_id else "updated"} successfully!', 'success')
            return redirect(url_for('admin_projects'))
        
        return render_template('admin/project_form.html', project=project)
    
    @app.route('/admin/project/<int:project_id>/delete', methods=['POST'])
    @admin_required
    def admin_project_delete(project_id):
        """Delete Project"""
        project = Project.query.get_or_404(project_id)
        
        # Delete associated images from filesystem
        for image in project.images:
            image_path = image.image_path.lstrip('/')
            filepath = os.path.join(app.root_path, image_path)
            if os.path.exists(filepath):
                os.remove(filepath)
        
        db.session.delete(project)
        db.session.commit()
        flash('Project deleted successfully!', 'success')
        return redirect(url_for('admin_projects'))
    
    @app.route('/admin/project/<int:project_id>/image/<int:image_id>/delete', methods=['POST'])
    @admin_required
    def admin_image_delete(project_id, image_id):
        """Delete Project Image"""
        project = Project.query.get_or_404(project_id)
        image = ProjectImage.query.get_or_404(image_id)
        
        if image.project_id != project_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Delete from filesystem
        image_path = image.image_path.lstrip('/')
        filepath = os.path.join(app.root_path, image_path)
        if os.path.exists(filepath):
            os.remove(filepath)
        
        db.session.delete(image)
        db.session.commit()
        
        return jsonify({'status': 'success'})
    
    # ================= BLOG MANAGEMENT =================
    
    @app.route('/admin/posts')
    @admin_required
    def admin_posts():
        """List all blog posts"""
        page = request.args.get('page', 1, type=int)
        posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(
            page=page, per_page=10
        )
        return render_template('admin/posts_list.html', posts=posts)
    
    @app.route('/admin/post/new', methods=['GET', 'POST'])
    @app.route('/admin/post/<int:post_id>/edit', methods=['GET', 'POST'])
    @admin_required
    def admin_post_form(post_id=None):
        """Create or Edit Blog Post"""
        post = None
        if post_id:
            post = BlogPost.query.get_or_404(post_id)
        
        projects = Project.query.all()
        
        if request.method == 'POST':
            if not post:
                post = BlogPost()
            
            post.title = request.form.get('title')
            post.content = request.form.get('content')
            post.published = request.form.get('published') == 'on'
            
            project_id = request.form.get('project_id')
            post.project_id = int(project_id) if project_id else None
            
            # Generate slug if new post
            if not post.slug:
                slug = post.generate_slug()
                counter = 1
                original_slug = slug
                while BlogPost.query.filter_by(slug=slug).first():
                    slug = f"{original_slug}-{counter}"
                    counter += 1
                post.slug = slug
            
            if not post.id:
                db.session.add(post)
            
            db.session.commit()
            flash(f'Post {"created" if not post_id else "updated"} successfully!', 'success')
            return redirect(url_for('admin_posts'))
        
        return render_template('admin/post_form.html', post=post, projects=projects)
    
    @app.route('/admin/post/<int:post_id>/delete', methods=['POST'])
    @admin_required
    def admin_post_delete(post_id):
        """Delete Blog Post"""
        post = BlogPost.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
        return redirect(url_for('admin_posts'))
    
    # ================= ERROR HANDLERS =================
    
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
