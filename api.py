from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user
from .models import Recipe, User
from . import db

bp = Blueprint('api', __name__)

@bp.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([{
        'id': r.id,
        'title': r.title,
        'description': r.description,
        'author': r.author.username,
        'created_at': r.created_at.isoformat(),
        'image_url': f'/uploads/{r.image_filename}' if r.image_filename else None
    } for r in recipes])

@bp.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return jsonify({
        'id': recipe.id,
        'title': recipe.title,
        'description': recipe.description,
        'ingredients': recipe.ingredients,
        'instructions': recipe.instructions,
        'author': recipe.author.username,
        'created_at': recipe.created_at.isoformat(),
        'comments': [{'author': c.author.username, 'content': c.content, 'date': c.created_at.isoformat()} for c in recipe.comments]
    })

@bp.route('/recipes', methods=['POST'])
@login_required
def create_recipe_api():
    if not request.is_json:
        abort(400, description="Request must be JSON")
    data = request.get_json()
    required = ['title', 'description', 'ingredients', 'instructions']
    if not all(k in data for k in required):
        abort(400, description="Missing fields")
    recipe = Recipe(
        title=data['title'],
        description=data['description'],
        ingredients=data['ingredients'],
        instructions=data['instructions'],
        user_id=current_user.id
    )
    db.session.add(recipe)
    db.session.commit()
    return jsonify({'id': recipe.id, 'message': 'Recipe created'}), 201

@bp.route('/users/<int:user_id>/recipes', methods=['GET'])
def get_user_recipes(user_id):
    user = User.query.get_or_404(user_id)
    recipes = Recipe.query.filter_by(user_id=user.id).all()
    return jsonify([{
        'id': r.id,
        'title': r.title,
        'description': r.description
    } for r in recipes])