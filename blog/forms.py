from django import forms

from blog.models import Comment, Post


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body')


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'publish')


class SearchForm(forms.Form):
    query = forms.CharField()
