from flask import Blueprint, render_template

# 블루프린트 정의
menu = Blueprint('menu', __name__)

# 시스템 관리 관련 라우트
@menu.route('/code_categories_list')
def code_categories_list():
    return render_template('code_categories_list.html')

@menu.route('/code_details_list')
def code_details_list():
    return render_template('code_details_list.html')

@menu.route('/menus_list')
def menus_list():
    return render_template('menus_list.html')

@menu.route('/users_list')
def users_list():
    return render_template('users_list.html')

@menu.route('/social_network_list')
def social_network_list():
    return render_template('social_network_list.html')

@menu.route('/login_log_list')
def login_log_list():
    return render_template('login_log_list.html')

# 영화 관리 관련 라우트
@menu.route('/movies_list')
def movies_list():
    return render_template('movies_list.html')

@menu.route('/movie_review_list')
def movie_review_list():
    return render_template('movie_review_list.html')

@menu.route('/movie_recommendations_list')
def movie_recommendations_list():
    return render_template('movie_recommendations_list.html')

@menu.route('/user_movie_info_list')
def user_movie_info_list():
    return render_template('user_movie_info_list.html')

# 영화인 관리 관련 라우트
@menu.route('/movie_person_list')
def movie_person_list():
    return render_template('movie_person_list.html')

# 이벤트 관리 관련 라우트
@menu.route('/event_list')
def event_list():
    return render_template('event_list.html')

# 인플루언서 관리 관련 라우트
@menu.route('/influencer_list')
def influencer_list():
    return render_template('influencer_list.html')

# 로그인 라우트
@menu.route('/login')
def login():
    return render_template('login.html')

# 마이페이지 관련 라우트
@menu.route('/user_reviews')
def user_reviews():
    return render_template('user_reviews.html')

@menu.route('/social_links')
def social_links():
    return render_template('social_links.html')

@menu.route('/custom_recommendations')
def custom_recommendations():
    return render_template('custom_recommendations.html')

@menu.route('/points_management')
def points_management():
    return render_template('points_management.html')

@menu.route('/notifications')
def notification_list():
    return render_template('notification_list.html')
