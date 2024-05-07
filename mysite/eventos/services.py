from datetime import datetime
import requests
from .models import EventEco, SymplaCategory, SymplaAddress, SymplaEvent, SymplaHost, SymplaParticipant
import pytz

utc = pytz.UTC


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
                id=dados['id'],
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
            id=dados['id'],
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


class DataService:
    sympla_api: SymplaApi

    def __init__(self):
        self.sympla_api = SymplaApi()

    def get_sympla_events(self):
        events = self.sympla_api.get_events()

        events.sort(reverse=True, key=lambda event: event.start_date)

        return events

    @staticmethod
    def get_database_events():
        events = list(EventEco.objects.all())

        events.sort(reverse=True, key=lambda event: event.start_date)

        return events

    def get_events(self):
        sympla_events = self.get_sympla_events()
        database_events = self.get_database_events()

        for database_event in database_events:
            for sympla_event in sympla_events:
                if sympla_event.id == database_event.id:
                    sympla_events.remove(sympla_event)  # Removendo o evento do array
                    break

        sympla_events.extend(database_events)

        sympla_events.sort(reverse=True, key=lambda event: event.start_date)

        return sympla_events

    def get_sympla_events_not_in_database(self):
        sympla_events = self.get_sympla_events()
        database_events = self.get_database_events()

        for database_event in database_events:
            for sympla_event in sympla_events:
                if sympla_event.id == database_event.id:
                    sympla_events.remove(sympla_event)  # Removendo o evento do array
                    break

        return sympla_events

    def get_events_categories(self):
        events = self.get_sympla_events_not_in_database()
        categories = []
        for event in events:
            category = event.category_prim.name
            if category not in categories:
                categories.append(category)
        return categories
    
    def get_sympla_participant_by_category(self, category):
        #buscar todos eventos sympla
        events = self.get_sympla_events_not_in_database()
        #obter id dos eventos que são da categoria selecionada
        events_id = []
        for event in events:
            if event.category_prim.name==category:
                events_id.append(event.id)
        #obter participantes dos eventos pelo id
        participants = None
        for id in events_id:
            participants = self.get_participants_by_event_id(id)
        #retornar participantes dos eventos
        return participants
    
    def get_valid_events(self):
        events = self.get_events()

        events.sort(reverse=True, key=lambda event: event.start_date)

        events = [event for event in events if event.is_valid()]

        return events

    def get_valid_event_by_id(self, event_id):
        event = EventEco.objects.filter(id=event_id).first()

        if not event:
            event = self.sympla_api.get_event_by_id(event_id)

        if not event.is_valid():
            return None

        return event

    def get_event_by_id(self, event_id):

        database_event = EventEco.objects.filter(id=event_id).first()
        if database_event:
            return database_event

        sympla_event = self.sympla_api.get_event_by_id(event_id)

        return sympla_event

    def get_participants_by_event_id(self, event_id):
        sympla_participants = self.sympla_api.get_participants_by_event_id(event_id)
        event = self.get_event_by_id(event_id)

        for participant in sympla_participants:
            participant.event = event

        return sympla_participants
