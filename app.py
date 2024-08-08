from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from menu import menu

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@10.0.66.94/moviedb'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@10.0.66.87/moviedb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 모델 정의
class CodeCategory(db.Model):
    __tablename__ = 'tb_code_categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Text, nullable=True)
    

class CodeDetail(db.Model):
    __tablename__ = 'tb_code_details'
    code_id = db.Column(db.Integer, primary_key=True)
    code_name = db.Column(db.String(100), nullable=False)
    code_value = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('tb_code_categories.category_id'), nullable=False)

class Event(db.Model):
    __tablename__ = 'tb_events'
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

class Influencer(db.Model):
    __tablename__ = 'tb_influencers'
    influencer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text, nullable=True)

class Menu(db.Model):
    __tablename__ = 'tb_menus'
    menu_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

class Movie(db.Model):
    __tablename__ = 'tb_movies'
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.String(500), nullable=True)

class User(db.Model):
    __tablename__ = 'tb_users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_type_cd = db.Column(db.String(1), nullable=True)
    signup_status_cd = db.Column(db.String(1), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey('tb_users.user_id'), nullable=True)
    updated_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    updated_by = db.Column(db.Integer, db.ForeignKey('tb_users.user_id'), nullable=True)

    # Foreign key relationships (self-referential)
    created_by_user = db.relationship('User', remote_side=[user_id], foreign_keys=[created_by])
    updated_by_user = db.relationship('User', remote_side=[user_id], foreign_keys=[updated_by])

class Log(db.Model):
    __tablename__ = 'tb_logs'
    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('tb_users.user_id'))
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

# 로그 기록 함수
def log_action(user_id, action):
    log_entry = Log(user_id=user_id, action=action)
    db.session.add(log_entry)
    db.session.commit()

# 라우트 설정

@app.route('/')
def home():
    return render_template('main_content.html')
# @app.route('/')
# def index():
#     return render_template('main.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('사용자 이름 또는 이메일이 이미 존재합니다.', 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        log_action(new_user.user_id, '회원가입 성공')

        flash('회원가입 성공! 로그인 해주세요.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.user_id
            log_action(user.user_id, '로그인 성공')
            flash('로그인 성공!', 'success')
            return redirect(url_for('index'))
        else:
            flash('사용자 이름이나 비밀번호가 잘못되었습니다.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    user_id = session.pop('user_id', None)
    if user_id:
        log_action(user_id, '로그아웃')
    flash('로그아웃 되었습니다.', 'info')
    return redirect(url_for('login'))

@app.route('/logs')
def logs():
    log_entries = Log.query.order_by(Log.timestamp.desc()).all()
    return render_template('logs.html', logs=log_entries)


@app.route('/create_code_categories', methods=['GET', 'POST'])
def create_code_categories():
    if request.method == 'POST':
        category_name = request.form['category_name']
        description = request.form['description']
        
        new_category = CodeCategory(category_name=category_name, description=description)
        db.session.add(new_category)
        db.session.commit()
        
        return redirect(url_for('search_code_categories'))

    categories = CodeCategory.query.all()
    return render_template('code_categories_list.html', categories=categories)

@app.route('/search_code_categories', methods=['GET', 'POST'])
def search_code_categories():
    # Initialize filter variables
    category_name = None
    description = None
    is_active = None

    # Check if the request method is POST
    if request.method == 'POST':
        category_id = request.form.get('search_category_id', '')
        category_name = request.form.get('search_category_name', '')
        description = request.form.get('search_description', '')
        is_active = request.form.get('is_active', None)

    # Build query with filters
    query = CodeCategory.query
    
    if category_id:
        query = query.filter(CodeCategory.category_id.ilike(f'%{category_id}%'))

    if category_name:
        query = query.filter(CodeCategory.category_name.ilike(f'%{category_name}%'))
    
    if description:
        query = query.filter(CodeCategory.description.ilike(f'%{description}%'))
    
    if is_active is not None:
        # Convert is_active to boolean for comparison
        is_active = bool(is_active)
        query = query.filter(CodeCategory.is_active == is_active)

    # Execute query and get results
    categories = query.all()
    
    return render_template('code_categories_list.html', categories=categories)

def create_app():
    app.register_blueprint(menu, url_prefix='/menu')  # 블루프린트 등록
    return app

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = create_app()
    app.run(debug=True)
