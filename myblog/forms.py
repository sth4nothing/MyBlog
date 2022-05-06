from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')


class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 200)])
    content = TextAreaField('正文',
                            render_kw={'id': 'editormd'},
                            validators=[DataRequired(),
                                        Length(1, 20000)])
    tags_str = StringField('标签', render_kw={'placeholder': '用,分割'})
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    content = StringField('评论', validators=[DataRequired(), Length(1, 500)])
    submit = SubmitField('提交')

class AdminLoginForm(FlaskForm):
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

class AdminForm(FlaskForm):
    sql = TextAreaField('SQL')
    submit = SubmitField('执行')
    export = SubmitField('导出')
