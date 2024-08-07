from django import forms
from .models import Videojuego, Consola, Comuna, Compra
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import re

class VideojuegoForm(forms.ModelForm):
    class Meta:
        model = Videojuego
        fields = ['nom_juego','stock_juego', 'descripcion', 'image', 'precio', 'id_consola']

class ConsolaForm(forms.ModelForm):
    class Meta:
        model = Consola
        fields = ['nombre']

class VideojuegoForm(forms.ModelForm):
    class Meta:
        model = Videojuego
        fields = ['nom_juego','stock_juego', 'descripcion', 'image', 'precio', 'id_consola']

class ComunaForm(forms.ModelForm):
    class Meta:
        model = Comuna
        fields = ['nombre']
        
def validate_letters_and_accents(value):
    pattern = r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Este campo solo puede contener letras y acentuaciones.'),
            code='invalid_characters'
        )

# Función de validación para verificar si una cadena contiene solo letras y acentuaciones, sin espacios
def validate_letters_and_accents_no_spaces(value):
    pattern = r'^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ]+$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('Este campo solo puede contener letras y acentuaciones, sin espacios.'),
            code='invalid_characters_no_spaces'
        )

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico')
    first_name = forms.CharField(label='Nombre', validators=[validate_letters_and_accents])
    last_name = forms.CharField(label='Apellido', validators=[validate_letters_and_accents])


    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'email': 'Correo electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña'
        }
        help_texts = {
            'password1': _("<br><br>Tu contraseña no puede ser demasiado similar a tu otra información personal.<br>"
                           "Tu contraseña debe contener al menos 8 caracteres.<br>"
                           "Tu contraseña no puede ser una contraseña común.<br>"
                           "Tu contraseña no puede ser completamente numérica."),
            
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['password1'].validators = []
        self.fields['password1'].help_text = self.Meta.help_texts['password1']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado como nombre de usuario.')
        return email

    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user

class AutentificacionForm(AuthenticationForm):
    username = forms.CharField(label=_('Correo electrónico'), max_length=256)

    error_messages = {
        'invalid_login': _(
            "Por favor, introduzca un %(username) válido y una contraseña correcta."
            "Tenga en cuenta que las mayúsculas y minúsculas se consideran diferentes."
        ),
        'inactive': _("Tu cuenta está inactiva."),
    }

class ResetPasswordForm(forms.Form):
    email = forms.EmailField()

    def save(self):
        email = self.cleaned_data['email']
        try:
            usuario = User.objects.get(username=email)
            return usuario
        except User.DoesNotExist:
            raise ValidationError("No hay ninguna cuenta asociada a ese correo electrónico.")


class CambiarContrasenaForm(forms.Form):
    password = forms.CharField(label='Nueva contraseña', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data
    



class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()

class DetallesPagoForm(forms.ModelForm):
    direccion_envio = forms.CharField(label = 'direccion_envio', max_length=100, required=True)
    tarjeta = forms.CharField(label='Número de tarjeta', max_length=16, required=True)
    cvv = forms.CharField(label='CVV', max_length=4, required=True)

    class Meta:
        model = Compra
        fields = ['direccion_envio', 'tarjeta', 'cvv']