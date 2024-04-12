from .models import EventEco, SymplaApi


class DataService:
    sympla_api: SymplaApi

    def __init__(self):
        self.sympla_api = SymplaApi()

    def get_events(self):
        sympla_events = self.sympla_api.get_events()
        database_events = EventEco.objects.all()
        print(database_events)

        for sympla_event in sympla_events:
            for database_event in database_events:
                if sympla_event.event_id == database_event.event_id:
                    sympla_event.event_eco = database_event

        sympla_events.sort(reverse=True, key=lambda event: event.start_date)

        return sympla_events

    def get_final_events(self):
        events = []

        for event in self.get_events():
            if event.event_eco:
                events.append(event.event_eco)
            else:
                events.append(event)

        events.sort(reverse=True, key=lambda event: event.start_date)

        events = [event for event in events if event.is_valid()]

        return events

    def get_final_event_by_id(self, event_id):
        event = EventEco.objects.filter(event_id=event_id).first()

        if not event:
            event = self.sympla_api.get_event_by_id(event_id)

        if not event.is_valid():
            return None

        return event

    def get_event_by_id(self, event_id):
        sympla_event = self.sympla_api.get_event_by_id(event_id)
        database_event = EventEco.objects.filter(event_id=event_id).first()

        if sympla_event and database_event:
            sympla_event.event_eco = database_event

        return sympla_event

    def get_participants_by_event_id(self, event_id):
        sympla_participants = self.sympla_api.get_participants_by_event_id(event_id)
        event = self.get_event_by_id(event_id)

        for participant in sympla_participants:
            participant.event = event

        return sympla_participants
