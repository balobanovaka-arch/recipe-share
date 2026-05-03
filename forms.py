from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=80)])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Такое имя пользователя уже занято. Выберите другое.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Эта почта уже зарегистрирована.')

class LoginForm(FlaskForm):
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RecipeForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Описание', validators=[DataRequired()])
    ingredients = TextAreaField('Ингредиенты (каждый с новой строки)', validators=[DataRequired()])
    instructions = TextAreaField('Инструкция приготовления', validators=[DataRequired()])
    image = FileField('Изображение рецепта', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Только картинки (jpg, png, jpeg)!')])
    submit = SubmitField('Опубликовать рецепт')

class CommentForm(FlaskForm):
    content = TextAreaField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Добавить комментарий')