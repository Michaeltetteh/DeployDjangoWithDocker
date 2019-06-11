from django import forms
from django.contrib.auth import get_user_model
from core.models import Vote,Movie

class VoteForm(forms.ModelForm):
    user = forms.ModelChoiceField(widget=forms.HiddenInput,
                                  quertset=get_user_model.objects.all(),
                                  disabled=True)
    movie = forms.ModelChoiceField(widget=forms.HiddenInput,
                                    queryset=Movie.object.all(),
                                    disabled=True)

    value = forms.ChoiceField(label='Vote',
                               widget=forms.RadioSelect,
                               choices=Vote.VALUE_CHOICES)

    class Meta:
        model = Vote
        fields = ('value','user','movie')