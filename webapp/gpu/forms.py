from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField


class SubscribeForm(FlaskForm):
    gpu_id = HiddenField("gpu_id")
    submit = SubmitField('Subscribe', render_kw={"class": "btn btn-primary"})


class UnsubscribeForm(FlaskForm):
    gpu_id = HiddenField("gpu_id")
    submit = SubmitField('Unsubscribe', render_kw={"class": "btn btn-secondary"})

    def validate_gpu_id(self, gpu_id):
        pass

