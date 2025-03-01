from ckeditor_uploader.fields import RichTextUploadingField
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    content = RichTextUploadingField()

    class Meta:
        model = Post
        fields = ['title', 'desc', 'category', 'content', 'tags']