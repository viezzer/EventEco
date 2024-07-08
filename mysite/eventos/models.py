from django.db import models


class EventEco(models.Model):

    id = models.IntegerField(primary_key=True, )
    sympla_event_id = models.IntegerField(null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=255)
    detail = models.TextField()
    private_event = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    image = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    host_name = models.CharField(max_length=255)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Evento Eco: {self.id}"

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def is_valid(self):
        return not self.cancelled and not self.private_event and self.published


class SymplaAddress:
    country: str
    address: str
    address_alt: str
    city: str
    address_num: str
    name: str
    state: str
    neighborhood: str
    zip_code: str
    lat: float
    lon: float

    def __init__(self, country, address, address_alt, city, address_num, name, lon,
                 state, neighborhood, zip_code, lat):
        self.country = country
        self.address = address
        self.address_alt = address_alt
        self.city = city
        self.address_num = address_num
        self.name = name
        self.lon = lon
        self.state = state
        self.neighborhood = neighborhood
        self.zip_code = zip_code
        self.lat = lat


class SymplaHost:
    name: str
    description: str

    def __init__(self, name, description):
        self.name = name
        self.description = description


class SymplaCategory:
    name: str

    def __init__(self, name):
        self.name = name


class SymplaEvent:

    id: int
    start_date: models.DateTimeField()
    end_date: models.DateTimeField()
    name: str
    detail: str
    private_event: int
    published: int
    cancelled: int
    image: str
    address: SymplaAddress
    host: SymplaHost
    category_prim: SymplaCategory
    category_sec: SymplaCategory
    url: str
    host_name: str
    category_name: str

    def __init__(self, id, start_date, end_date, name, detail, private_event, published,
                 cancelled, image, address, host, category_prim, category_sec, url, host_name, category_name):

        self.id = id
        self.start_date = start_date
        self.end_date = end_date
        self.name = name
        self.detail = detail
        self.private_event = private_event
        self.published = published
        self.cancelled = cancelled
        self.image = image
        self.address = address
        self.host = host
        self.category_prim = category_prim
        self.category_sec = category_sec
        self.url = url
        self.host_name = host_name
        self.category_name = category_name

    def is_valid(self):
        return not self.cancelled and not self.private_event and self.published

    def __str__(self):
        return f"Evento Sympla: {self.id}"


class SymplaParticipant:
    participant_id: int
    event_id: int
    order_id: str
    order_status: str
    order_date: str
    order_updated_date: str
    order_approved_date: str
    ticket_number: str
    ticket_num_qr_code: str
    ticket_name: str
    ticket_sale_price: float
    first_name: str
    last_name: str
    email: str
    event: SymplaEvent

    def __init__(self, participant_id, event_id, order_id, order_status, order_date,
                 order_updated_date, order_approved_date, ticket_number, ticket_num_qr_code,
                 ticket_name, ticket_sale_price, first_name, last_name, email, event=None):

        self.participant_id = participant_id
        self.event_id = event_id
        self.order_id = order_id
        self.order_status = order_status
        self.order_date = order_date
        self.order_updated_date = order_updated_date
        self.order_approved_date = order_approved_date
        self.ticket_number = ticket_number
        self.ticket_num_qr_code = ticket_num_qr_code
        self.ticket_name = ticket_name
        self.ticket_sale_price = ticket_sale_price
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.event = event
