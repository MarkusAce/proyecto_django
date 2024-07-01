from django import forms
from .models import Videojuego, Consola, Comuna, Usuario

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

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

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'a_paterno', 'a_materno', 'direccion', 'email1', 'cel1', 'password','id_comuna']
    id_comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(),empty_label="Selecciona una comuna")

# class CambiarContrasenaForm(forms.ModelForm):
#     class Meta:
#         model = Usuario
#         fields = ['password']  # Solo incluye el campo 'password' para cambiar la contrasena
#         widgets = {
#             'password': forms.PasswordInput(),  # Renderiza el campo de contrasena como una entrada de contrasena
#         }


from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario

class ResetPasswordForm(forms.Form):
    email = forms.EmailField()

    def save(self):
        email = self.cleaned_data['email']
        try:
            usuario = Usuario.objects.get(email1=email)
            return usuario
        except Usuario.DoesNotExist:
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



class AutentificacionForm(AuthenticationForm):
    username = forms.CharField(label=_('Correo electrónico'), max_length=256)

    error_messages = {
        'invalid_login': _(
            "Por favor, introduzca un %(username) válido y una contraseña correcta."
            "Tenga en cuenta que las mayúsculas y minúsculas se consideran diferentes."
        ),
        'inactive': _("Tu cuenta está inactiva."),
    }