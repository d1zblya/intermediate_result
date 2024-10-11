import os
from flask_login import LoginManager, login_required, logout_user
from data import db_session
from flask import Flask, render_template, redirect
from flask_restful import Api
from api.reviews_resources import CommonReview, DetailReview, GetUserReviews, WriteReview
from api.items_resources import CommonItem, DetailItem, GetCriterionsProduct, SellerItems
from api.pages_resources import ProductPage, ReviewsPage
from api.user_resources import UserInfo, UserRank, CountProducts, SelerInfo
from api.rating_resources import NumberRating, AverageRating
from api.criterions_resources import GetCriterions


app = Flask(__name__)
app.config['SECRET_KEY'] = 'our_secret_key'

api = Api(app)

api.add_resource(CommonReview, '/api/reviews') # метод get/post
api.add_resource(DetailReview, '/api/reviews/<int:review_id>')
api.add_resource(GetUserReviews, '/api/reviews/user/<int:current_user_id>')
api.add_resource(WriteReview, '/api/review')

api.add_resource(CommonItem, '/api/items') # метод get/post
api.add_resource(DetailItem, '/api/items/<string:name_of_item>')
api.add_resource(GetCriterionsProduct, '/api/items/criterions/<string:category>')

api.add_resource(UserInfo, '/api/user/info/<user_id>')
api.add_resource(UserRank, '/api/user/rank/<int:user_id>')

api.add_resource(SelerInfo, '/api/seller/info/<int:user_id>')
api.add_resource(SellerItems, '/api/seller/items/<int:user_id>')
api.add_resource(CountProducts, '/api/seller/count-products/<int:user_id>')

api.add_resource(ProductPage, '/api/page/product')
api.add_resource(ReviewsPage, '/api/page/review/<int:item_id>')

api.add_resource(NumberRating, '/api/rating/count/<item_id>')
api.add_resource(AverageRating, '/api/rating/average/<int:item_id>')

api.add_resource(GetCriterions, '/api/item/criterions/<int:item_id>')


login_manager = LoginManager()
login_manager.init_app(app)

from pages import (
    registration,
    login,
    passwordreset,
    reviews,
    lcab,
    review,
    products
)


@app.route('/')
def main_page():
    return render_template(
        'main.html',
        background=True
        )


@app.route('/logout')
@login_required
def logout():
    """Выход из профиля"""

    logout_user()

    return redirect('/')


if __name__ == '__main__':
    db_session.global_init('db\db_swipe_csat-schem.db')  # - указать адрес БД
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
