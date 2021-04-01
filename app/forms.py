from flask_wtf import Form
from wtforms import TextField
from wtforms import TextAreaField
from wtforms import BooleanField
from wtforms import RadioField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import validators
from wtforms.validators import DataRequired, Email
from app import models,db

class register(Form):
    firstname = TextField('First Name', validators=[DataRequired()])
    surname = TextField('Surname', validators=[DataRequired()])
    email = TextField('Email address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class SignIn(Form):
    email = TextField('Email address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class changepassword(Form):
    currentpassword = PasswordField('Current Password', validators=[DataRequired()])
    newpassword = PasswordField('New Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm New Password', validators=[DataRequired()])

class filterProducts(Form):
    filter = SelectField('Size', validators=[DataRequired()], choices = ['Releavance', 'Price - Low to High', 'Price - High to Low'])

def get_sizes(productid):
    sizes_avaliable = []
    p = models.Products.query.get(productid)
    if p.xsstocklevel > 0:
        sizes_avaliable.append("Extra Small (XS)")
    if p.sstocklevel > 0:
        sizes_avaliable.append("Small (S)")
    if p.mstocklevel > 0:
        sizes_avaliable.append("Medium (M)")
    if p.lstocklevel > 0:
        sizes_avaliable.append("Large (L)")
    if p.xlstocklevel > 0:
        sizes_avaliable.append("Extra Large (XL)")
    return sizes_avaliable

class PickSize(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(1))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(1)
        return form

class PickSize2(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(2))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(2)
        return form

class PickSize3(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(3))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(3)
        return form

class PickSize4(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(4))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(4)
        return form

class PickSize5(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(5))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(5)
        return form

class PickSize6(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(6))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(6)
        return form

class PickSize7(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(7))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(7)
        return form

class PickSize8(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(8))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(8)
        return form

class PickSize9(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(9))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(9)
        return form

class PickSize10(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(10))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(10)
        return form

class PickSize11(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(11))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(11)
        return form

class PickSize12(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(12))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(12)
        return form

class PickSize13(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(13))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(13)
        return form

class PickSize14(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(14))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(14)
        return form

class PickSize15(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(15))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(15)
        return form

class PickSize16(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(16))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(16)
        return form

class PickSize17(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(17))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(17)
        return form

class PickSize18(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(18))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(18)
        return form

class PickSize19(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(19))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(19)
        return form

class PickSize20(Form):
    size = SelectField('Size', validators=[DataRequired()], choices = get_sizes(20))
    @classmethod
    def new(cls):
        # Instantiate the form
        form = cls()
        # Update the choices for the size field
        form.size.choices = get_sizes(20)
        return form
