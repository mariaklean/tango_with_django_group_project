from django import forms
from rango.models import Review, UserProfile
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(initial=0, max_value=5, min_value=0)
    review = forms.Textarea()

    class Meta:
        model = Review
        fields = ('rating', 'review',)