from flask import render_template, redirect, request, Blueprint
from blog.models.model import Post

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    """Handle the rendering of home page"""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=2, page=page)
    return render_template('home.html', posts=posts);


@main.route("/about")
def about():
    return render_template("about.html", title='About');

