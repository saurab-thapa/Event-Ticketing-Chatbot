def is_event_ticketing_question(text: str) -> bool:
    topic_words = [
        "event",
        "events",
        "ticket",
        "tickets",
        "booking",
        "book",
        "buy",
        "purchase",
        "seat",
        "seats",
        "seating",
        "venue",
        "show",
        "concert",
        "conference",
        "timing",
        "date",
        "price",
        "pricing",
        "refund",
        "cancel",
        "reschedule",
        "pass",
        "entry",
    ]
    check_text = text.lower()
    return any(word in check_text for word in topic_words)
