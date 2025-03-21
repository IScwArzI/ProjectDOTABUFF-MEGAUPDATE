from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))

class AdminUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))

@app.route('/')
def index():
    heroes = Hero.query.all()
    return render_template('index.html', heroes=heroes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = AdminUser.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('admin'))
        else:
            flash('Неверный логин или пароль', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    heroes = Hero.query.all()
    return render_template('admin.html', heroes=heroes)

@app.route('/add_hero', methods=['POST'])
@login_required
def add_hero():
    name = request.form['name']
    description = request.form['description']
    image_url = request.form['image_url']
    new_hero = Hero(name=name, description=description, image_url=image_url)
    db.session.add(new_hero)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete_hero/<int:hero_id>', methods=['POST'])
@login_required
def delete_hero(hero_id):
    hero = Hero.query.get_or_404(hero_id)
    db.session.delete(hero)
    db.session.commit()
    flash('Герой успешно удалён', 'success')
    return redirect(url_for('admin'))

@app.route('/hero/<int:hero_id>')
def hero_detail(hero_id):
    hero = Hero.query.get_or_404(hero_id)
    return render_template('hero_detail.html', hero=hero)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)