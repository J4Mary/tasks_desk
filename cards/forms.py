from django.forms import ModelForm

from cards import models


class CardForm(ModelForm):
    class Meta:
        model = models.Card
        fields = ('text', 'assigned_to')
