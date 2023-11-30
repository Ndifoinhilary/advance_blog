from django import forms
from blog import models as model


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModeForm):
    class Meta:
        model = model.Comment
        fields = ["name", "email", "body"]
