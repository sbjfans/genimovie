from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from menu import menu

from models import db, Influencer, Notification, CodeCategory, CodeDetail, Menu, User, Movie, MovieImage, Personnel, MoviePersonnel, Recommendation, Review, UserMovieInfo, UserPlan, Event, PointTransaction, Log
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@10.0.66.94/moviedb'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@10.0.66.87/moviedb'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

db.init_app(app)  # Initialize SQLAlchemy with the app

# 파일업로드 경로 설정
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

# 로그 기록 함수
def log_action(user_id, action):
    log_entry = Log(user_id=user_id, action=action)
    db.session.add(log_entry)
    db.session.commit()

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

        print('분류코드 저장::')

        category_name = request.form['category_name']
        description = request.form['description']
        is_active = request.form['is_active']

        if is_active=='on':
            is_active=1
        else :
            is_active=0    

        print('category_name::'+category_name)
        print('description::'+description)
        print('is_active::'+str(is_active))
        
        new_category = CodeCategory(category_name=category_name, description=description, is_active=is_active)
        db.session.add(new_category)
        db.session.commit()
        
        return redirect(url_for('search_code_categories'))

    categories = CodeCategory.query.all()
    return render_template('code_categories_list.html', categories=categories)

@app.route('/search_code_categories', methods=['GET', 'POST'])
def search_code_categories():

    print('코드분류 조회::')

    category_id = ''
    category_name = ''
    description = ''
    is_active = ''

    if request.method == 'POST':
        category_id = request.form.get('search_category_id', '')
        category_name = request.form.get('search_category_name', '')
        description = request.form.get('search_description', '')
        is_active = request.form.get('is_active', '')

        print('category_id::'+category_id)
        print('category_name::'+category_name)
        print('description::'+description)
        print('is_active::'+str(is_active))

    query = CodeCategory.query

    if category_id:
        query = query.filter(CodeCategory.category_id.ilike(f'%{category_id}%'))
    if category_name:
        query = query.filter(CodeCategory.category_name.ilike(f'%{category_name}%'))
    if description:
        query = query.filter(CodeCategory.description.ilike(f'%{description}%'))
    if is_active != '':
        query = query.filter(CodeCategory.is_active == is_active)

    categories = query.all()

    print('query='+str(query))   
    '''
    query=SELECT tb_code_categories.category_id AS tb_code_categories_category_id, tb_code_categories.category_name AS tb_code_categories_category_name, tb_code_categories.description AS tb_code_categories_description, tb_code_categories.is_active AS tb_code_categories_is_active
    FROM tb_code_categories
    '''

    return render_template('code_categories_list.html', 
                           categories=categories, 
                           search_category_id=category_id, 
                           search_category_name=category_name, 
                           search_description=description, 
                           search_is_active=is_active)


@app.route('/select_category_list', methods=['GET'])
def select_categories_list():
    print('코드분류목록조회::')

    # Query all categories
    categories = CodeCategory.query.all()

    # Convert the query result to a list of dictionaries
    category_list = [
        {
            'category_id': category.category_id,
            'category_name': category.category_name
        }
        for category in categories
    ]

    # Print the query for debugging
    print('categories=' + str(category_list))

    # Return the list of categories as JSON
    return jsonify({'categories': category_list})


@app.route('/create_influencer', methods=['POST'])
def create_influencer():
    if request.method == 'POST':
        name = request.form['name']
        bio = request.form['bio']
        img_path=''
        
        # Handle the file upload
        if 'photo' not in request.files:
            return "No file part"
        file = request.files['photo']
        if file.filename == '':
            return "No selected file"
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_path = '/'+UPLOAD_FOLDER
            # Save to database
            new_influencer = Influencer(name=name, bio=bio, img_path=img_path, img_nm=filename)
            db.session.add(new_influencer)
            db.session.commit()
            
            return redirect(url_for('search_influencers'))
    
    return render_template('influencers_list.html')

@app.route('/search_influencers', methods=['GET', 'POST'])
def search_influencers():

    print('인플루언서 조회::')
    
    name = ''

    if request.method == 'POST':
        
        name = request.form.get('search_name', '')
        
        print('name::'+name)
       
    query = Influencer.query

    if name:
        query = query.filter(Influencer.name.ilike(f'%{name}%'))
    

    influencers = query.all()

    print('query='+str(query))   
   
    return render_template('influencers_list.html',     
                           influencers=influencers,                        
                           search_name=name 
                          )





# 영화 조회
@app.route('/search_movies', methods=['GET', 'POST'])
def search_movies():
    print('영화 조회::')

    movie_id = ''
    title = ''
    director_name = ''

    if request.method == 'POST':
        movie_id = request.form.get('search_movie_id', '')
        title = request.form.get('search_title', '')
        director_name = request.form.get('search_director_name', '')

        print('movie_id::' + movie_id)
        print('title::' + title)
        print('director_name::' + director_name)

    query = db.session.query(
        Movie.movie_id,
        Movie.title,
        Movie.genre,
        Movie.release_date,
        db.func.coalesce(db.func.round(db.func.avg(Review.rating) * 2) / 2, 0).label('average_rating'),
        Personnel.name.label('director_name'),
        MovieImage.image_url  # 이미지 URL 추가
    ).outerjoin(Review, Movie.movie_id == Review.movie_id)\
     .outerjoin(MoviePersonnel, Movie.movie_id == MoviePersonnel.movie_id)\
     .outerjoin(Personnel, db.and_(MoviePersonnel.personnel_id == Personnel.personnel_id, Personnel.role_code == 'director'))\
     .outerjoin(MovieImage, Movie.movie_id == MovieImage.movie_id).group_by(Movie.movie_id, Personnel.name, MovieImage.image_url)  

    if movie_id:
        query = query.filter(Movie.movie_id.ilike(f'%{movie_id}%'))
    if title:
        query = query.filter(Movie.title.ilike(f'%{title}%'))
    if director_name:
        query = query.filter(Personnel.name.ilike(f'%{director_name}%'))

    movies = query.all()

    print('query=' + str(query))

    return render_template('movies_list.html',
                           movies=movies,
                           search_movie_id=movie_id,
                           search_title=title,
                           search_director_name=director_name)



@app.route('/search_movies_pop', methods=['GET', 'POST'])
def search_movies_pop():
    print('영화 팝업 조회::')

    movie_id = ''
    title = ''
    director_name = ''

    if request.method == 'POST':
        movie_id = request.form.get('search_movie_id', '')
        title = request.form.get('search_title', '')
        director_name = request.form.get('search_director_name', '')

        print('movie_id::' + movie_id)
        print('title::' + title)
        print('director_name::' + director_name)

    # 영화와 이미지 테이블 조인
    query = db.session.query(
        Movie.movie_id,
        Movie.title,
        Movie.genre,
        Movie.release_date,
        db.func.coalesce(db.func.round(db.func.avg(Review.rating) * 2) / 2, 0).label('average_rating'),
        Personnel.name.label('director_name'),
        MovieImage.image_url  # 이미지 URL 추가
    ).outerjoin(Review, Movie.movie_id == Review.movie_id)\
     .outerjoin(MoviePersonnel, Movie.movie_id == MoviePersonnel.movie_id)\
     .outerjoin(Personnel, db.and_(MoviePersonnel.personnel_id == Personnel.personnel_id, Personnel.role_code == 'director'))\
     .outerjoin(MovieImage, Movie.movie_id == MovieImage.movie_id).group_by(Movie.movie_id, Personnel.name, MovieImage.image_url)  

    if movie_id:
        query = query.filter(Movie.movie_id.ilike(f'%{movie_id}%'))
    if title:
        query = query.filter(Movie.title.ilike(f'%{title}%'))
    if director_name:
        query = query.filter(Personnel.name.ilike(f'%{director_name}%'))

    movies = query.all()

    print('query=' + str(query))

    return render_template('movies_list_pop.html',
                           movies=movies,
                           search_movie_id=movie_id,
                           search_title=title,
                           search_director_name=director_name)




@app.route('/save_recommendations', methods=['POST'])
def save_recommendations():
    data = request.json
    user_id = data['user_id']
    movie_plan_ids = data['movie_plan_ids']
    
    try:
        for movie_plan_id in movie_plan_ids:
            recommendation = Recommendation(
                user_id=user_id,
                movie_plan_id=movie_plan_id,
                is_recommended=True,
                created_by=user_id
            )
            db.session.add(recommendation)
        db.session.commit()
        return jsonify({"message": "Recommendations saved successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

def create_app():
    app.register_blueprint(menu, url_prefix='/menu')  # 블루프린트 등록
    return app

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app = create_app()
    
    app.run(debug=True)
