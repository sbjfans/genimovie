from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from menu import menu


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@10.0.66.94/moviedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 모델 정의
class CodeCategory(db.Model):
    __tablename__ = 'tb_code_categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

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

# 라우트 설정
@app.route('/')
def index():
    return render_template('main.html')



def create_app():

    app.register_blueprint(menu, url_prefix='/menu')  # 블루프린트 등록
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
