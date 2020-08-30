from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserChangeForm, SignupForm
from django.utils.translation import ugettext_lazy as _
from .models import User

# class MyUserChangeForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = '__all__'


# class MyUserCreationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('username',)


class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = SignupForm

    list_display = ('username', 'is_admin')
    list_filter = ('is_admin', 'is_superuser')
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin', 'is_superuser',)}),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

# Register your models here.
admin.site.register(User, MyUserAdmin)