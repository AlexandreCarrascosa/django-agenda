from datetime import date, datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Eventos(models.Model):
  title = models.CharField(max_length=100, verbose_name='Título')
  description = models.TextField(blank=True, null=True)
  event_date = models.DateTimeField(verbose_name='Data do Evento')
  creation_date = models.DateTimeField(auto_now=True, verbose_name='Criado em')
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Meta:
    db_table = 'eventos'

  def __str__(self):
    return self.title


  def get_event_date(self):
    return self.event_date.strftime('%d/%m/%Y - %H:%M' )
  
  def get_data_input_evento(self):
    return self.event_date.strftime('%Y-%m-%dT%H:%m')
  
  def get_evento_atrasado(self):
    print(self.event_date, datetime.now())
    if self.event_date < datetime.now():
      return True
    else:
      return False