"""Trip planner: the structured itinerary.

To be used to extract one typed itinerary from the conversation.

Please note `cost` is a STRING, not a number, so that
"unknown" is something the itinerary can actually say, and so a price can carry
where it came from. If it were a float the model would have to invent a figure
to fill it, and a made-up price looks exactly like a real one.
"""

from typing import Literal

from pydantic import BaseModel, Field


class Activity(BaseModel):
    """One thing the traveller does."""
    time: str = Field(description="When it starts, e.g. '09:30' or 'morning'")
    name: str = Field(description="What it is, e.g. 'Museum of Fine Arts'")
    kind: Literal["sight", "food", "event", "travel", "other"] = Field(
        description="Which tool this came from: sight, food, event, travel, other")
    cost: str = Field(
        description="'free' only when something actually says it is free; a price "
                    "a tool gave you, marked with where it came from, like "
                    "'$45-120 (Ticketmaster)' or '$27 (blog, unconfirmed)'; or "
                    "'unknown'. Most things will be 'unknown' — that is the honest "
                    "answer, and an unknown price is never 0.")
    source: str = Field(description="The URL this came from, or 'none' if there isn't one")


# TODO: write DayPlan. One day of the trip: a date, what the weather said, and a
# list of Activity. An itinerary is a list of days, each holding a list of
# activities — one level more nesting than W03a.2.
class DayPlan(BaseModel):
    """One day of the trip."""
    date: str = Field(description="The date for the day trip in YYYY-MM-DD format, e.g. '2026-10-03'")
    weather: str = Field(description="What the get_weather tool reported for this day, or 'unknown' if weather was not available")
    activities: list[Activity] = Field(description="The activities planned for this day, in chronological order")

# TODO: write Itinerary. The city, a list of DayPlan, and an `unknowns` list of
# everything the tools could not confirm. Give every field a Field(description=...):
# those descriptions are what the model reads when it fills the model in.
class Itinerary(BaseModel):
    """A complete plan for a trip."""
    city: str = Field(
        description="The city where the trip takes place"
    )
    days: list[DayPlan] = Field(description="The days of the trip, each containing that day's activities")
    unknowns: list[str] = Field(description="Things the available tools could not confirm, such as "
                    "unknown prices, missing weather, or unavailable information"
    )


ITINERARIES = []


def build_itinerary(model, result) -> Itinerary:
    """Extract a structured itinerary from a finished planning conversation.

    This is `file_ticket` from W03b.1 pointed at a trip. Build the transcript from
    result["messages"], call model.with_structured_output(Itinerary) on it, append
    to ITINERARIES, and return it.
    """
    # TODO: implement
    transcript = "\n".join(f"{type(m).__name__}: {m.text}" for m in result["messages"] if m.text)
    record = model.with_structured_output(Itinerary).invoke(f"Create an itinerary from this travel planning conversation:\n\n{transcript}")
    ITINERARIES.append(record)
    return record