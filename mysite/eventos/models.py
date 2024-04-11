from django.db import models

# Api Sympla: Controle e atualização dos dados vindos do Sympla.
# Evento Sympla: Classe espelhada do Sympla.
# Evento Eco: Classe editável com base no Sympla.
# Anfitrião: Classe espelhada do Sympla.
# Categoria: Classe espelhada do Sympla.
# Local: Classe espelhada do Sympla.
# Pedido: Classe espelhada do Sympla.
# Cliente: Classe espelhada do Sympla.

class Api(models.Model):
    access_token = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    base_url = models.URLField(max_length=200)

    def __str__(self):
        return f"URL: {self.base_url}"

class EventoSympla(models.Model):
    id = models.IntegerField(primary_key=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=255)
    detail = models.TextField()
    private_event = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    image = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Evento Sympla - ID: {self.id}, Nome: {self.name}"

class EventoEco(models.Model):
    id = models.IntegerField(primary_key=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=255)
    detail = models.TextField()
    private_event = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    image = models.URLField(max_length=255)
    url = models.URLField(max_length=255)

    def __str__(self):
        return f"Evento Eco - ID: {self.id}, Nome: {self.name}"
    
class Local(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address_num = models.CharField(max_length=20)
    address_alt = models.CharField(max_length=255, blank=True, null=True)
    neighborhood = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=255)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"Local - {self.name}, {self.address}, {self.city}, {self.state}"
    
class Pedido(models.Model):
    id = models.IntegerField(primary_key=True)
    event_id = models.IntegerField()
    order_id = models.CharField(max_length=255)
    order_status = models.CharField(max_length=255)
    order_date = models.DateTimeField()
    order_updated_date = models.DateTimeField()
    order_approved_date = models.DateTimeField(null=True, blank=True)
    order_discount = models.CharField(max_length=255)
    ticket_number = models.CharField(max_length=255)
    ticket_num_qr_code = models.CharField(max_length=255)
    ticket_name = models.CharField(max_length=255)
    pdv_user = models.CharField(max_length=255)
    ticket_sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido - ID: {self.id}, Evento ID: {self.event_id}, Order ID: {self.order_id}"
    
class Cliente(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    
class Categoria(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Anfitriao(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField("date published")


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)