from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# Here you have to import the User model from your app!
from .models import User

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','fullname','email', 'dob')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'fullname', 'email', 'password', 'dob', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
        model = User
        list_display = ('username', 'email','fullname','is_Moderator','is_admin','is_active','is_superuser','has_subscribed','dob')
        list_filter = ( 'email','username','is_Moderator','is_active','is_admin','is_superuser','has_subscribed')  
        filter_horizontal = ()                                                                                                                                         
        fieldsets =  ((None, {'fields': ('username','email','fullname')}),('Permissions', {'fields': ('is_active','is_admin', 'is_Moderator')}),
               ('Personal', {'fields': ('has_subscribed','dob')}),
        )                      
        add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'password1', 'password2')}
        ),)
        search_fields = ('fullname','email','username' )
        ordering = ('username', )

#admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

