from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from flask_wtf.file import FileField, FileRequired  # <--------------
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class WorksForm(FlaskForm):
    time = StringField('Дата/Время', validators=[DataRequired()])
    photo = FileField()   # <-------------
    address = StringField('Адрес', validators=[DataRequired()])
    mph = IntegerField("Почасовая ставка")
    min_pay = IntegerField("Часы минимальной оплаты")
    amount = IntegerField("Количество человек")
    description = TextAreaField('Описание')
    submit = SubmitField('Создать')
