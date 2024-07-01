from django.shortcuts import render,redirect, get_object_or_404
from .models import Videojuego, Consola, Carrito, ElementoCarrito, Usuario
from .forms import VideojuegoForm, ConsolaForm, UsuarioForm, ComunaForm 
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from .forms import ResetPasswordForm






from django.contrib.auth import views as auth_views

def crear_videojuego(request):
    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_videojuegos')
    
    else:
        form = VideojuegoForm()
    return render(request,'formulario_videojuegos.html',{'form':form})

def crear_consola(request):
    if request.method == 'POST':
        form = ConsolaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('crear_consola')
        
    else:
        form = ConsolaForm()
    return render(request,'formulario_consola.html',{'form':form})

def lista_videojuegos(request, consola=None):
    if consola:
        videojuegos = Videojuego.objects.filter(id_consola=consola).order_by,('nom_juego')
    else:
        videojuegos = Videojuego.objects.all().order_by('id_consola','nom_juego')
    context ={
        'videojuegos': videojuegos,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'lista_videojuegos.html', context)

def lista_videojuegos1(request):
    videojuegos = Videojuego.objects.all()
    context ={
        'videojuegos': videojuegos,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'listar-juego-cliente.html', context)

def editar_videojuego(request, pk):
    videojuego = get_object_or_404(Videojuego, pk=pk)

    if request.method == 'POST':
        form = VideojuegoForm(request.POST, request.FILES, instance=videojuego)
        if form.is_valid():
            form.save()
            return redirect('lista_videojuegos')
    else:
        form = VideojuegoForm(instance=videojuego)

    return render(request, 'editar_videojuego.html',{'form':form})

def lista_inicio(request):
    videojuegos = Videojuego.objects.order_by('id_consola', 'nom_juego')
    context ={
        'videojuegos': videojuegos,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'inicio.html', context)

def eliminar_videojuego(request, pk):
    videojuego = get_object_or_404(Videojuego, pk=pk)
    if request.method == 'POST':
        videojuego.delete()
        return redirect('lista_videojuegos')
    return render(request, 'confirmar_eliminacion.html',{'videojuego':videojuego})

def nosotros(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'nosotros.html', context)
def lista_videojuegos_consola(request, consola):
    consola_obj = Consola.objects.get(nombre=consola)

    videojuegos = Videojuego.objects.filter(id_consola=consola_obj).order_by('nom_juego')

    context = {
        'videojuegos': videojuegos,
        'consola': consola,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'lista_videojuegos_consola.html', context)

def juego_detalle(request, juego_id):
    videojuego = get_object_or_404(Videojuego, pk=juego_id)
    juegos_recomendados = Videojuego.objects.filter(id_consola=videojuego.id_consola).exclude(pk=juego_id).order_by('?')[:2]

    context = {
        'videojuego': videojuego,
        'juegos_recomendados': juegos_recomendados,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'juego.html', context)

def buscar_juegos(request):
    query = request.GET.get('q','')
    juegos = Videojuego.objects.filter(nom_juego__icontains=query)
    context = {
        'query':query,
        'juegos': juegos,

    }
    return render(request, 'resultado_busqueda.html', context)

def nosotros(request):
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'nosotros.html', context)

@login_required
def agregar_al_carrito(request, videojuego_id):
    videojuego = get_object_or_404(Videojuego, id_producto = videojuego_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    elemento_carrito, creado = ElementoCarrito.objects.get_or_create(
        carrito=carrito, videojuego=videojuego, defaults={'precio': videojuego.precio}
    )

    if not creado:
        elemento_carrito.cantidad +=1
        elemento_carrito.save()

    return redirect('ver_carrito')
@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    elementos_carrito = ElementoCarrito.objects.filter(carrito=carrito)
    total_precio = sum(item.precio * item.cantidad for item in elementos_carrito)
    iva = total_precio * 0.19
    subtotal = total_precio - iva
    context = {
        'elementos_carrito': elementos_carrito,
        'total_precio': total_precio,
        'iva':iva,
        'subtotal':subtotal,
    }
    return render(request, 'carrito.html', context)

@login_required
def eliminar_del_carrito(request, elemento_carrito_id):
    elemento_carrito = get_object_or_404(ElementoCarrito, id=elemento_carrito_id)
    elemento_carrito.delete()
    return redirect('ver_carrito')

def registrar(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            nuevo_usuario = form.save(commit=False)
            nuevo_usuario.password = form.cleaned_data['password']
            nuevo_usuario.save()
            return redirect('lista_inicio')
    else:
        form = UsuarioForm()

    context = {
        'form': form,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'registrar.html', context)

def crear_comuna(request):
    if request.method == 'POST':
        form = ComunaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_inicio')
    else:
        form = ComunaForm()
    
    context = {
        'form': form,
    }
    return render(request, 'crear_comuna.html',context)


from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import ResetPasswordForm, CambiarContrasenaForm
from .models import Usuario
from .tokens import account_activation_token
import ssl
import smtplib
from email.message import EmailMessage

def resetear_contrasena(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            try:
                usuario = form.save()
                token = account_activation_token.make_token(usuario)
                uid = urlsafe_base64_encode(force_bytes(usuario.pk))
                url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

                # Crear el mensaje de correo
                subject = 'Restablecimiento de contraseña'
                body = render_to_string('password_reset_email.html', {
                    'user': usuario,
                    'url': url,
                })
                
                email = 'megagames185@gmail.com'
                contrasena = 'gnlcnnkxuajkwnjp'
                destinatario = usuario.email1

                # Crear objeto de mail
                em = EmailMessage()
                em['From'] = email
                em['To'] = destinatario
                em['Subject'] = subject
                em.set_content(body)

                # Añadir SSL (extra de seguridad)
                context = ssl.create_default_context()

                # Iniciar sesión y enviar el mail
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email, contrasena)
                    smtp.sendmail(email, destinatario, em.as_string())

                return redirect('lista_inicio')  # Cambia esto según sea necesario
            except ValidationError as e:
                form.add_error('email', e)
                pass
    else:
        form = ResetPasswordForm()

    return render(request, 'resetear_contrasena.html', {'form': form})



from django.shortcuts import render, redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .forms import CambiarContrasenaForm
from .models import Usuario
from .tokens import account_activation_token

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = CambiarContrasenaForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect('lista_inicio')  # Redirige a la página de inicio de sesión
        else:
            form = CambiarContrasenaForm()
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'password_reset_invalid.html')


from django.shortcuts import render,redirect, get_object_or_404
from .models import Videojuego, Consola, Carrito, ElementoCarrito
from .forms import VideojuegoForm, ConsolaForm,ComunaForm,  AutentificacionForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import AutentificacionForm

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AutentificacionForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('lista_inicio')
            else:
                error_message = 'Nombre de usuario o contraseña incorrectos'
                print(f"Error message: {error_message}")
                messages.error(request, error_message)
        else:
            for field in form:
                for error in field.errors:
                    print(f"Error in field {field.label}: {error}")
    else:
        form = AutentificacionForm()
    return render(request, 'ingresar.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('lista_inicio')