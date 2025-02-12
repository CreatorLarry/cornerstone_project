from django.contrib.auth.forms import UserCreationForm
from django import forms
from main.models import Member

from .models import Event, Blog, Sermon


class MemberRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[
        ('member', 'Member'), ('leader', 'Leader'), ('pastor', 'Pastor'), ('admin', 'Admin')], required=True
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
        required=True
    )

    class Meta:
        model = Member
        fields = ['first_name', 'second_name', 'other_name', 'email', 'phone', 'profile_picture',
                  'gender', 'dob', 'bio', 'department', 'role', 'password1', 'password2']


class MemberLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            "first_name",
            "second_name",
            "other_name",
            "phone",
            "gender",
            "dob",
            "email",
            "department",
            "role",
            "profile_picture",
        ]
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
            "gender": forms.Select(choices=[("M", "Male"), ("F", "Female")]),
            "department": forms.Select(choices=[
                ("kayo", "KAYO"),
                ("mothers_union", "Mothers' Union"),
                ("kama", "KAMA"),
                ("children", "Children's")
            ]),
            "role": forms.Select(choices=[
                ("member", "Member"),
                ("leader", "Leader"),
                ("clergy", "Clergy")
            ]),
        }


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

