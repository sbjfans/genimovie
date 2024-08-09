from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
    category_id = db.Column(db.Integer, db.ForeignKey('tb_code_categories.category_id'), nullable=False)
    code_name = db.Column(db.String(100), nullable=False)
    code_value = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.String(10), nullable=True)
    category = db.relationship('CodeCategory', backref=db.backref('code_details', lazy=True))

class Menu(db.Model):
    __tablename__ = 'tb_menus'
    menu_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.String(10), nullable=True)
    created_by = db.Column(db.Integer, nullable=False)
    updated_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())





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







class Movie(db.Model):
    __tablename__ = 'tb_movies'
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.DateTime, nullable=True)
    media_review = db.Column(db.Text, nullable=True)

class MovieImage(db.Model):
    __tablename__ = 'tb_movie_images'
    image_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('tb_movies.movie_id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    movie = db.relationship('Movie', backref=db.backref('images', lazy=True))

class Personnel(db.Model):
    __tablename__ = 'tb_personnel'
    personnel_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    role_code = db.Column(db.String(10), nullable=True)

class MoviePersonnel(db.Model):
    __tablename__ = 'tb_movie_personnel'
    movie_id = db.Column(db.Integer, db.ForeignKey('tb_movies.movie_id'), primary_key=True)
    personnel_id = db.Column(db.Integer, db.ForeignKey('tb_personnel.personnel_id'), primary_key=True)
    role = db.Column(db.String(100), nullable=False)
    movie = db.relationship('Movie', backref=db.backref('personnel', lazy=True))
    personnel = db.relationship('Personnel', backref=db.backref('movies', lazy=True))    




class Recommendation(db.Model):
    __tablename__ = 'tb_recommendations'
    recommendation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    movie_plan_id = db.Column(db.Integer, nullable=False)
    is_recommended = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, nullable=False)
    updated_by = db.Column(db.Integer, nullable=True)

class Review(db.Model):
    __tablename__ = 'tb_reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('tb_movies.movie_id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    movie = db.relationship('Movie', backref=db.backref('reviews', lazy=True))

class UserMovieInfo(db.Model):
    __tablename__ = 'tb_user_movie_info'
    user_movie_info_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    view_count = db.Column(db.Integer, default=0)
    rating = db.Column(db.Integer, nullable=True)
    is_recommended = db.Column(db.Boolean, default=False)

class UserPlan(db.Model):
    __tablename__ = 'tb_user_plan'
    tb_user_plan_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, nullable=False)
    recommendations_received = db.Column(db.Integer, default=0)
    recommendations_declined = db.Column(db.Integer, default=0)

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
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, nullable=False)
    updated_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

class Notification(db.Model):
    __tablename__ = 'tb_notifications'
    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class PointTransaction(db.Model):
    __tablename__ = 'tb_point_transactions'
    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_by = db.Column(db.Integer, nullable=False)
    updated_by = db.Column(db.Integer, nullable=True)

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