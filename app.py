import os
from flask import Flask, render_template
from config import Config
from extensions import db, login_manager
from roles import Role
from models import User

from blueprints.auth.routes import bp as auth_bp
from blueprints.student.routes import bp as student_bp
from blueprints.counselor.routes import bp as counselor_bp
from blueprints.admin.routes import bp as admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
        # seed admin jika belum ada
        if not User.query.filter_by(role=Role.ADMIN.value).first():
            admin = User(name='Admin', email='admin@kampus.ac.id', role=Role.ADMIN.value)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(counselor_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
