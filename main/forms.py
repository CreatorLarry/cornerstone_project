from django.contrib.auth.forms import UserCreationForm
from django import forms
from main.models import ContactMessage

from .models import Event, Blog, Sermon, Comment



class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'image']


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image']


class SermonForm(forms.ModelForm):
    class Meta:
        model = Sermon
        exclude = ['date']
        fields = ['title', 'preacher', 'date', 'audio_file', 'video_url', 'description']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "content"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject"]
