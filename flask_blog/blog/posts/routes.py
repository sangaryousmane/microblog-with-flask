from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from blog import db
from blog.models.model import Post
from blog.posts.forms import PostForm

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=['POST', 'GET'])
@login_required
def new_post():
    """Create a post"""
    form = PostForm()
    if form.validate_on_submit():
        all_posts = Post(title=form.title.data,
                         content=form.content.data, author=current_user);
        db.session.add(all_posts);
        db.session.commit();
        flash("The post has been created!", 'success');
        return redirect(url_for('main.home'))
    return render_template('create_post.html', form=form,
                           legend="Create a new post", title='New Post');


@posts.route("/post/<int:post_id>",
             methods=['GET', 'POST', 'PUT', 'DELETE'])
def post(post_id):
    """Navigate to a post"""
    all_posts = Post.query.get_or_404(post_id);
    return render_template('post.html',
                           post=all_posts, title=all_posts.title);


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """Get Post by ID and Update afterwards"""
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    form = PostForm();
    if form.validate_on_submit():
        post.title = form.title.data;
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated successfully", 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title;
        form.content.data = post.content;
    return render_template("create_post.html", legend="Update Post",
                           title="Update Post", form=form)


@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    """DELETE A POST"""
    post = Post.query.get_or_404(post_id);
    if post.author != current_user:
        abort(403);

    db.session.delete(post);
    db.session.commit();
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'));
