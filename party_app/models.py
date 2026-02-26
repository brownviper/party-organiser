from datetime import date, time
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel, Column, String, Text


# Common base model for the Party resource.
# Defines shared fields used by both the database and form models.
class PartyBase(SQLModel):
    party_date: date
    party_time: time
    invitation: str = Field(
        sa_column=Column(Text), min_length=10
    )  # Column(Text) affects PostgreSQL (not SQLite); min_length is enforced by Pydantic.
    venue: str = Field(
        sa_column=Column(String(100))
    )  # Column(String(100)) affects PostgreSQL (not SQLite).


# Database model for the Party resource.
# Inherits from PartyBase and represents the actual table, including relationships.
class Party(PartyBase, table=True):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True)
    gifts: List["Gift"] = Relationship(
        back_populates="party"
    )  # Defines ORM relationship: party.gifts returns associated Gift objects.
    guests: List["Guest"] = Relationship(
        back_populates="party"
    )  # Defines ORM relationship: party.guests returns associated Guest objects.


# Form model for the Party resource.
# Used by FastAPI to validate and process incoming form data for Party operations.
class PartyForm(PartyBase):
    pass


# Common base model for the Gift resource.
# Contains shared fields used by both the database and form models.
class GiftBase(SQLModel):
    gift_name: str = Field(sa_column=Column(String(100)))
    price: Decimal = Field(decimal_places=2, ge=0)  # Decimal constraints enforced by Pydantic (not SQLite).
    link: Optional[str]
    party_id: UUID = Field(
        default=None, foreign_key="party.uuid"
    )  # Defines a foreign key connecting the gift to a party at the database level.


# Database model for the Gift resource.
# Inherits from GiftBase and represents the gift table, including its relationship to Party.
class Gift(GiftBase, table=True):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True)
    party: Party = Relationship(
        back_populates="gifts"
    )  # Defines ORM relationship: gift.party returns the associated Party object.


# Form model for the Gift resource.
# Used for validating and processing incoming gift data via FastAPI.
class GiftForm(GiftBase):
    pass


# Common base model for the Guest resource.
# Defines shared fields used by both the database and form models.
class GuestBase(SQLModel):
    name: str = Field(sa_column=Column(String(100)))
    attending: bool = False
    party_id: UUID = Field(
        default=None, foreign_key="party.uuid"
    )  # Defines a foreign key connecting the guest to a party at the database level.


# Database model for the Guest resource.
# Inherits from GuestBase and maps to the guest table, including its relationship to Party.
class Guest(GuestBase, table=True):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True)
    party: Party = Relationship(
        back_populates="guests"
    )  # Establishes ORM relationship: guest.party returns the associated Party object.


# Form model for the Guest resource.
# Used by FastAPI for validating and processing incoming guest data.
class GuestForm(GuestBase):
    pass