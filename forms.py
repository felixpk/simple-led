from flask_wtf import FlaskForm
from wtforms import SelectField

from animations import ANIMATIONS


class AnimationForm(FlaskForm):
    choices = [(a, ANIMATIONS[a].name) for a in ANIMATIONS]
    animation = SelectField(u'Animation', choices=choices)
