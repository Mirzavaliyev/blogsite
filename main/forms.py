from django import forms
from .models import Comment, Post, Category

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Izohingizni yozing...'}),
        }
        labels = {
            'content': 'Izoh',
        }
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']
        widgets = {
            'title':forms.TextInput(attrs={'class': 'form.control','placeholder':'Post sarlavhasi'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Post mazmuni'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'})

        }
        labels = {
            'title': 'Sarlavha',
            'content': 'Mazmun',
            'category': 'Kategoriya',
            'image': 'Rasm',
        }