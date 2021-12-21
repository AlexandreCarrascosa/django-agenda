from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.http.response import Http404, JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from .models import Eventos

from datetime import datetime, time, timedelta


def login_user(request):
  return render(request, 'login.html')

def logout_user(request):
  logout(request)
  return redirect('/')

def submit_login(request):

  if request.POST:
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('/')
    
    else:
      messages.error(request, "Usuário e/ou Senha incorretos!")

    return redirect('/')
  
def currentUser(request):
  return render(request, 'agenda.html', user = request.user)

@login_required(login_url='/login/')
def listEventos(request):
  user = request.user
  current_date = datetime.now() - timedelta(hours=1)
  
  evento = Eventos.objects.filter(user=user,
                                  event_date__gt = current_date)
  response = {'evento': evento}

  return render(request, 'agenda.html', response)

@login_required(login_url='/login/')
def evento(request):
  
  id_evento = request.GET.get('id')
  dados = {}
  
  if id_evento:
    dados['evento'] = Eventos.objects.get(id=id_evento)
  
  return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def submit_evento(request):
  if request.POST:
    title = request.POST.get('title')
    event_date = request.POST.get('event_date')
    description = request.POST.get('description')
    user = request.user
    
    id_evento = request.POST.get('id_evento')
    
    if id_evento:
      evento = Eventos.objects.get(id=id_evento)
      
      if evento.user == user:
        evento.title = title
        evento.event_date = event_date
        evento.description = description
        evento.save()
      
    else:    
      Eventos.objects.create(title=title,
                            event_date = event_date,
                            description=description,
                            user = user)
    
    
  return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
  user = request.user
  
  try:
    evento = Eventos.objects.get(id=id_evento)
  except Exception:
    raise Http404()

  if user == evento.user:
    evento.delete()
  
  else:
    raise Http404()
    
  return redirect('/')


@login_required(login_url='/login/')
def json_lista_evento(request):
  user = request.user
  evento = Eventos.objects.filter(user=user).values('id', 'title')
  
  return JsonResponse(list(evento), safe=False)