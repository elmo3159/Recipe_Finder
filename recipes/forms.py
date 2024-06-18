from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="ユーザー名",
        max_length=150,
        help_text="必須。150文字以下。文字、数字、および@/./+/-/_ のみ使用可能。"
    )
    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
        help_text=(
            "パスワードは他の個人情報と似ていてはいけません。\n"
            "パスワードは少なくとも8文字である必要があります。\n"
            "パスワードは一般的に使用されているものであってはいけません。\n"
            "パスワードは完全に数字だけであってはいけません。"
        )
    )
    password2 = forms.CharField(
        label="パスワード確認",
        widget=forms.PasswordInput,
        help_text="確認のため、もう一度同じパスワードを入力してください。"
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ("username", "email")
