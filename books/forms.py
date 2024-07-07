from django import forms
from books.models import RATING_CHOICES, Books, Comment


class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = '__all__'
        exclude = ['date_of_issue']
        
class CommentForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=RATING_CHOICES, required=True)
    body = forms.CharField(widget=forms.Textarea(), required=True)

    class Meta:
        model = Comment
        fields = ['rating', 'body']