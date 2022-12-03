from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, FloatField
from wtforms.validators import InputRequired, Optional, URL, NumberRange

class Add_Cupcake_Form(FlaskForm):
    flavor = StringField('Name', validators=[InputRequired(message="Name cannot be blank")])
    size = SelectField('Size', choices=[("small", "Small"), ("medium", "Medium"), ("large", "Large")])
    rating = FloatField('Rating', validators=[InputRequired(message="Rating cannot be blank")])
    image = StringField('Image', validators=[Optional(), URL()])
    

class Edit_Cupcake_Form(FlaskForm):
    
    image = StringField('Image', validators=[Optional(), URL()])
    size = SelectField('Size', choices=[("small", "Small"), ("medium", "Medium"), ("large", "Large")])
    rating = FloatField('Rating', validators=[InputRequired(message="Rating cannot be blank")])