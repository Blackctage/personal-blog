from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, FileInput, Textarea, ModelChoiceField, DateTimeInput, Select, DateInput, \
    URLField, URLInput
from django import forms
from .models import Post, ArticlesType, Work, Comment


class EditPostForm(ModelForm):
    articles_type = ModelChoiceField(queryset=ArticlesType.objects.all(),
                                                widget=Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['title', 'photo_or_video', 'summary', 'isbn', 'articles_type', 'publish_date', 'status']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'title',
            }),
            'photo_or_video': FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'photo_or_video',
            }),
            'summary': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'summary',
            }),
            'isbn': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'isbn',
            }),
            'publish_date': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'published date',
            }),
            'status': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'status',
                'choices': 'LOAN_STATUS',
            }),
        }

        LOAN_STATUS = (
            ('h', 'Hidden'),
            ('a', 'Available'),
        )


class EditWorkForm(ModelForm):
    class Meta:
        model = Work
        fields = '__all__'
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'title',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'description',
            }),
            'tags': TextInput(attrs={
                'class': 'form-control',
            }),
            'link': URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'website',
            })
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': TextInput(attrs={
                'class': 'form-control form-control--textarea',
                'placeholder': 'Текст комментария',
            })
        }
