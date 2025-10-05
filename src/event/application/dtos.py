class EventDto:
    name: str
    location: str
    created_at: str
    start_date: str
    end_date: str
    tickets_available: int
    organizer_id: int
    staffs_id: list[str] | None
    id: int | None = None


class PaginatedEventsDto:
    event_list: list[EventDto]
    total_event_count: int
