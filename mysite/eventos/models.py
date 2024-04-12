from datetime import datetime
from django.db import models
import requests
from django_ckeditor_5.fields import CKEditor5Field
import pytz

utc=pytz.UTC


class EventEco(models.Model):

    event_id = models.IntegerField(primary_key=True, )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=255)
    detail = CKEditor5Field(config_name='extends')
    private_event = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    image = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    preset = models.IntegerField()

    def __str__(self):
        return f"Evento Eco: {self.event_id}"

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

    event_id: int
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
    event_eco: EventEco

    def __init__(self, event_id, start_date, end_date, name, detail, private_event, published,
                 cancelled, image, address, host, category_prim, category_sec, url, event_eco=None):

        self.event_id = event_id
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
        self.event_eco = event_eco

    def __str__(self):
        if self.event_eco:
            return f"Evento Sympla: {self.event_id},"
        return f"Evento Sympla: {self.event_id}"

    def is_valid(self):
        return not self.cancelled and not self.private_event and self.published


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


class SymplaApi:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__access_token = '3f91929265b642131da64207388623a52fdd5c970093ce9102b44e4b87b82fc4'
        self.__url = "https://api.sympla.com.br"
        self.__headers = {
            's_token': self.__access_token,
        }

    def __str__(self):
        return f"URL: {self.__url}"

    def get_events(self):
        url = self.__url + "/public/v4/events"
        response = requests.request("GET", url, headers=self.__headers)
        # print(json.dumps(response, indent=4))

        if response.status_code != 200:
            return []

        response = response.json()

        events = []
        for dados in response['data']:
            category_prim = SymplaCategory(name=dados['category_prim']['name'])
            category_sec = SymplaCategory(name=dados['category_sec']['name'])
            address = SymplaAddress(
                country=dados['address']['country'],
                address=dados['address']['address'],
                address_alt=dados['address']['address_alt'],
                city=dados['address']['city'],
                address_num=dados['address']['address_num'],
                name=dados['address']['name'],
                lon=dados['address']['lon'],
                state=dados['address']['state'],
                neighborhood=dados['address']['neighborhood'],
                zip_code=dados['address']['zip_code'],
                lat=dados['address']['lat']
            )

            host = SymplaHost(name=dados['host']['name'], description=dados['host']['description'])
            event = SymplaEvent(
                event_id=dados['id'],
                start_date=utc.localize(datetime.strptime(dados['start_date'], '%Y-%m-%d %H:%M:%S')),
                end_date=utc.localize(datetime.strptime(dados['end_date'], '%Y-%m-%d %H:%M:%S')),
                name=dados['name'],
                detail=dados['detail'],
                private_event=dados['private_event'],
                published=dados['published'],
                cancelled=dados['cancelled'],
                image=dados['image'],
                address=address,
                host=host,
                category_prim=category_prim,
                category_sec=category_sec,
                url=dados['url'],
            )

            events.append(event)

        return events

    def get_event_by_id(self, event_id):
        url = self.__url + f"/public/v4/events/{event_id}"
        response = requests.request("GET", url, headers=self.__headers)
        # print(json.dumps(response, indent=4))

        if response.status_code != 200:
            return None

        dados = response.json()['data']

        category_prim = SymplaCategory(name=dados['category_prim']['name'])
        category_sec = SymplaCategory(name=dados['category_sec']['name'])
        address = SymplaAddress(
            country=dados['address']['country'],
            address=dados['address']['address'],
            address_alt=dados['address']['address_alt'],
            city=dados['address']['city'],
            address_num=dados['address']['address_num'],
            name=dados['address']['name'],
            lon=dados['address']['lon'],
            state=dados['address']['state'],
            neighborhood=dados['address']['neighborhood'],
            zip_code=dados['address']['zip_code'],
            lat=dados['address']['lat']
        )

        host = SymplaHost(name=dados['host']['name'], description=dados['host']['description'])
        event = SymplaEvent(
            event_id=dados['id'],
            start_date=utc.localize(datetime.strptime(dados['start_date'], '%Y-%m-%d %H:%M:%S')),
            end_date=utc.localize(datetime.strptime(dados['end_date'], '%Y-%m-%d %H:%M:%S')),
            name=dados['name'],
            detail=dados['detail'],
            private_event=dados['private_event'],
            published=dados['published'],
            cancelled=dados['cancelled'],
            image=dados['image'],
            address=address,
            host=host,
            category_prim=category_prim,
            category_sec=category_sec,
            url=dados['url']
        )

        return event

    def get_participants_by_event_id(self, event_id):
        url = self.__url + f"/public/v3/events/{event_id}/participants"
        # print(json.dumps(response, indent=4))
        response = requests.request("GET", url, headers=self.__headers)

        if response.status_code != 200:
            return []

        response = response.json()

        participants = []
        for dados in response['data']:
            participant = SymplaParticipant(
                participant_id=dados['id'],
                event_id=dados['event_id'],
                order_id=dados['order_id'],
                order_status=dados['order_status'],
                order_date=dados['order_date'],
                order_updated_date=dados['order_updated_date'],
                order_approved_date=dados['order_approved_date'],
                ticket_number=dados['ticket_number'],
                ticket_num_qr_code=dados['ticket_num_qr_code'],
                ticket_name=dados['ticket_name'],
                ticket_sale_price=dados['ticket_sale_price'],
                first_name=dados['first_name'],
                last_name=dados['last_name'],
                email=dados['email']
            )

            participants.append(participant)

        return participants
