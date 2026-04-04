from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User
from app.models.tutorial import Tutorial, TutorialStep
from app.models.resource import Resource, ResourceTag
from app.models.community import DiscussionPost, PostComment

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Mail', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        from app.models.user import User
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken')

    def validate_email(self, email):
        from app.models.user import User
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email has been registered')


class TutorialCategoryForm(FlaskForm):
    name = StringField('Category name', validators=[DataRequired(), Length(max=64)])
    slug = StringField('URL identifier', validators=[DataRequired(), Length(max=64)])
    description = TextAreaField('Describe')
    sort_order = IntegerField('Sort', default=0)
    submit = SubmitField('Save')

class ResourceCategoryForm(FlaskForm):
    name = StringField('Category name', validators=[DataRequired(), Length(max=64)])
    slug = StringField('URL identifier', validators=[DataRequired(), Length(max=64)])
    icon = StringField('Icon class', validators=[Length(max=50)])
    submit = SubmitField('Save')

class SiteSettingForm(FlaskForm):
    value = TextAreaField('Value')
    submit = SubmitField('Update')


class TutorialForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    slug = StringField('URL identifier', validators=[DataRequired(), Length(max=200)])
    summary = TextAreaField('Summary')
    content = TextAreaField('Content', validators=[DataRequired()])
    difficulty = SelectField('难度', choices=[('beginner'),('intermediate'),('advanced')])
    estimated_minutes = IntegerField('Estimated minutes', default=10)
    is_published = BooleanField('Release')
    category_id = SelectField('Classification', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.models.tutorial import TutorialCategory
        self.category_id.choices = [(c.id, c.name) for c in TutorialCategory.query.order_by(TutorialCategory.name).all()]

class TutorialStepForm(FlaskForm):
    step_number = IntegerField('Step number', validators=[DataRequired()])
    title = StringField('Step title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    code_snippet = TextAreaField('code example')
    image_url = StringField('Image URL', validators=[Length(max=500)])
    submit = SubmitField('Save')


class ResourceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('describe')
    type = SelectField('Type', choices=[('ebook'),('video'),('sample'),('tool')])
    download_url = StringField('Download link', validators=[Length(max=500)])
    external_link = StringField('External links', validators=[Length(max=500)])
    file_size = StringField('File size', validators=[Length(max=50)])
    is_featured = BooleanField('Recommend')
    category_id = SelectField('Classification', coerce=int, validators=[DataRequired()])
    tags = StringField('Tag', validators=[Length(max=200)])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from app.models.resource import ResourceCategory
        self.category_id.choices = [(c.id, c.name) for c in ResourceCategory.query.all()]

class ResourceTagForm(FlaskForm):
    name = StringField('Tag name', validators=[DataRequired(), Length(max=50)])
    slug = StringField('URL identifier', validators=[DataRequired(), Length(max=50)])
    submit = SubmitField('Save')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('content', validators=[DataRequired()])
    category = SelectField('Classification', choices=[('general'),('help'),('showcase')])
    submit = SubmitField('release')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post comment')