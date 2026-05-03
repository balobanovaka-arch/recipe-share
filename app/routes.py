import os
import requests
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from . import db
from .models import User, Recipe, Comment
from .forms import RegistrationForm, LoginForm, RecipeForm, CommentForm

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(9).all()
    return render_template('index.html', recipes=recipes)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        flash('Login failed. Check email and password.', 'danger')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/recipe/new', methods=['GET', 'POST'])
@login_required
def create_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            f = form.image.data
            filename = secure_filename(f.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            f.save(filepath)
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            image_filename=filename,
            user_id=current_user.id
        )
        db.session.add(recipe)
        db.session.commit()
        flash('Your recipe has been posted!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_recipe.html', form=form)

@bp.route('/recipe/<int:id>')
def recipe_detail(id):
    recipe = Recipe.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(content=form.content.data, user_id=current_user.id, recipe_id=recipe.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment added!', 'success')
        return redirect(url_for('main.recipe_detail', id=recipe.id))
    comments = Comment.query.filter_by(recipe_id=recipe.id).order_by(Comment.created_at.desc()).all()
    return render_template('recipe_detail.html', recipe=recipe, comments=comments, form=form)

@bp.route('/profile')
@login_required
def profile():
    user_recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(Recipe.created_at.desc()).all()
    return render_template('profile.html', user=current_user, recipes=user_recipes)

@bp.route('/random-meal')
def random_meal():
    try:
        response = requests.get('https://www.themealdb.com/api/json/v1/1/random.php', timeout=5)
        data = response.json()
        meal = data['meals'][0] if data['meals'] else None
    except:
        meal = None
        flash('Could not fetch random meal from external API.', 'warning')
    return render_template('random_meal.html', meal=meal)