from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField

# カスタムユーザー取得
User = get_user_model()

# アカウント登録
class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ("username",)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        User.objects.filter(username=username, is_active=False).delete()
        if User.objects.filter(username=username).count() != 0:
            raise forms.ValidationError("このアカウント名は既に登録されています。")
        return username
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致していません。")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# アカウント情報変更（未実装）
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("username", "password", "is_active", "is_admin", "is_superuser")
    
    def clean_password(self):
        return self.initial["password"]