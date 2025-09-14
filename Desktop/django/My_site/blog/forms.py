from .models import Comment
from django import forms

# this is to recommend posts by email.
# Form: Allow to build standard forms by defining fields and validations.

# ModelForm: Allows to build forms tied to model instances.

# Forms can reside anywhere in the Django project. The convention is to place them inside a forms.py files for each applcation.


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea
    )
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class SearchForm(forms.Form):
    query= forms.CharField()
    
