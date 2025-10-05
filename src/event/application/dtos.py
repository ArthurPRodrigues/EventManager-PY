from event.domain.event import Event


class PaginatedEventsDto:
    event_list: list[Event]
    total_event_count: int
