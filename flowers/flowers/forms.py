from django import forms
from .models import *
from .validators import (
    validate_name, validate_description, validate_price,
    validate_quantity, validate_email, validate_password
)


class CategoriesForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        validators=[validate_name],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tur nomini kiriting'
        }),
        label='Tur nomi'
    )
    definition = forms.CharField(
        max_length=300,
        validators=[validate_description],
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': "yangi tur haqida ma'lumot kiriting"
        }),
        label="Tur haqida ma'lumot"
    )

    def create(self):
        species = Categories.objects.create(**self.cleaned_data)
        return species

    def update(self, species):
        species.name = self.cleaned_data.get('name')
        species.definition = self.cleaned_data.get('definition')
        species.save()


class FlowerForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        validators=[validate_name],
        widget=forms.TextInput(attrs={
            'placeholder': 'gul nomini kiriting',
            'class': 'form-control'
        }),
        label='Gul nomi'
    )
    description = forms.CharField(
        validators=[validate_description],
        widget=forms.Textarea(attrs={
            'placeholder': "gul haqida ma'lumot kiriting",
            'class': 'form-control'
        }),
        label='Gul haqida'
    )
    price = forms.IntegerField(
        validators=[validate_price],
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        }),
        label='Gul narxi'
    )
    published = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'checked': 'checked'
        }),
        label="Mavjud yoki yo'q"
    )
    type = forms.ModelChoiceField(
        queryset=Categories.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label="Bog'langan gul turi"
    )
    quantity = forms.IntegerField(
        validators=[validate_quantity],
        widget=forms.NumberInput(attrs={
            "placeholder": "gul nechtaligi",
            "class": "form-control"
        })
    )

    def create(self):
        flowers = Flowers.objects.create(**self.cleaned_data)
        return flowers

    def update(self, flowers):
        flowers.name = self.cleaned_data.get('name')
        flowers.price = self.cleaned_data.get('price')
        flowers.published = self.cleaned_data.get('published')
        flowers.type = self.cleaned_data.get('type')
        flowers.quantity = self.cleaned_data.get('quantity')
        flowers.description = self.cleaned_data.get('description')
        flowers.save()


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        validators=[validate_name],
        widget=forms.TextInput(attrs={
            'id': 'form3Example1cg',
            'class': 'form-control form-control-lg'
        })
    )
    email = forms.EmailField(
        validators=[validate_email],
        widget=forms.EmailInput(attrs={
            'id': 'form3Example3cg',
            'class': 'form-control form-control-lg'
        })
    )
    password = forms.CharField(
        min_length=8,
        validators=[validate_password],
        widget=forms.PasswordInput(attrs={
            'id': 'form3Example4cg',
            'class': 'form-control form-control-lg'
        })
    )
    password_confirm = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'id': 'form3Example4cdg',
            'class': 'form-control form-control-lg'
        })
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        validators=[validate_name],
        widget=forms.TextInput(attrs={
            'id': 'form3Example1cg',
            'class': 'form-control form-control-lg'
        })
    )
    password = forms.CharField(
        min_length=8,
        validators=[validate_password],
        widget=forms.PasswordInput(attrs={
            'id': 'form3Example4cg',
            'class': 'form-control form-control-lg'
        })
    )


class CommentForm(forms.Form):
    text = forms.CharField(
        max_length=1200,
        validators=[validate_description],
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
        }),
        label="Izohingizni qoldiring:"
    )

    def update(self, comments):
        comments.text = self.cleaned_data.get('text')
        comments.save()
