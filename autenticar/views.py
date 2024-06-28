from django.shortcuts import render, redirect
from .forms import RegistrationForm

# Create your views here.
def ingresar(request):
    return render(request, 'ingresar.html')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Aquí puedes procesar los datos del formulario, por ejemplo, crear un nuevo usuario
            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # password = form.cleaned_data['password']
            # Crear el usuario, etc.
            return redirect('success')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})