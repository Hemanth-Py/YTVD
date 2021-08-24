from django.forms import ModelForm

from .models import *

class link_form(ModelForm):

    class Meta:
        model = yt_link
        fields = '__all__'