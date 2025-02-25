from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional


class Gender(Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    PREFER_NOT_TO_SAY = "N"


class PaymentMethod(Enum):
    CREDIT_CARD = "CC"
    DEBIT_CARD = "DC"
    BANK_TRANSFER = "BT"
    PAYPAL = "PP"


@dataclass
class PersonalInfo:
    first_name: str
    last_name: str
    birth_date: date
    gender: Gender
    nationality: str
    tax_id: str
    social_security_number: str

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_age(self) -> int:
        today = date.today()
        return today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day))


@dataclass
class ContactInfo:
    email: str
    phone_number: str
    alternative_phone: Optional[str] = None

    def mask_email(self) -> str:
        return f"{self.email[:3]}...@{self.email.split('@')[1]}"

    def mask_phone(self) -> str:
        return f"***{self.phone_number[-4:]}"


@dataclass
class Address:
    street: str
    street_number: str
    city: str
    state: str
    postal_code: str
    country: str
    apartment: Optional[str] = None

    def get_full_address(self) -> str:
        address_parts = [
            self.street,
            self.street_number,
            self.apartment,
            self.postal_code,
            self.city,
            self.state,
            self.country
        ]
        return ", ".join(part for part in address_parts if part)


@dataclass
class CardInfo:
    card_number: str
    card_holder_name: str
    card_expiry_month: int
    card_expiry_year: int
    card_cvv: str

    def mask_card_number(self) -> str:
        return f"****-****-****-{self.card_number[-4:]}"

    def is_expired(self) -> bool:
        today = date.today()
        return (today.year > self.card_expiry_year or
                (today.year == self.card_expiry_year and
                 today.month > self.card_expiry_month))


@dataclass
class BankInfo:
    bank_name: str
    account_number: str
    routing_number: str
    swift_code: Optional[str] = None
    iban: Optional[str] = None

    def mask_account_number(self) -> str:
        return f"****{self.account_number[-4:]}"


@dataclass
class PaymentInfo:
    payment_method: PaymentMethod
    card_info: Optional[CardInfo] = None
    bank_info: Optional[BankInfo] = None


@dataclass
class Preferences:
    preferred_language: str = "en"
    marketing_consent: bool = False
    newsletter_subscription: bool = False


@dataclass
class Person:
    id: str
    personal_info: PersonalInfo
    contact_info: ContactInfo
    address: Address
    payment_info: PaymentInfo
    preferences: Preferences
    billing_address: Optional[Address] = None
    created_at: date = field(default_factory=date.today)
    updated_at: date = field(default_factory=date.today)
    is_active: bool = True

    def mask_sensitive_data(self) -> dict:
        """Retorna una versión de los datos con información sensible enmascarada"""
        masked_data = {
            "id": self.id,
            "name": self.personal_info.get_full_name(),
            "email": self.contact_info.mask_email(),
            "phone": self.contact_info.mask_phone(),
        }

        if self.payment_info.card_info:
            masked_data["card_number"] = self.payment_info.card_info.mask_card_number()

        if self.payment_info.bank_info:
            masked_data["bank_account"] = self.payment_info.bank_info.mask_account_number()

        return masked_data


# Ejemplo de uso
if __name__ == "__main__":
    personal_info = PersonalInfo(
        first_name="John",
        last_name="Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        nationality="US",
        tax_id="123-45-6789",
        social_security_number="987-65-4321"
    )

    contact_info = ContactInfo(
        email="john.doe@example.com",
        phone_number="+1234567890"
    )

    address = Address(
        street="Main Street",
        street_number="123",
        city="New York",
        state="NY",
        postal_code="10001",
        country="United States"
    )

    card_info = CardInfo(
        card_number="4111111111111111",
        card_holder_name="John Doe",
        card_expiry_month=12,
        card_expiry_year=2025,
        card_cvv="123"
    )

    payment_info = PaymentInfo(
        payment_method=PaymentMethod.CREDIT_CARD,
        card_info=card_info
    )

    preferences = Preferences()

    person = Person(
        id="P12345",
        personal_info=personal_info,
        contact_info=contact_info,
        address=address,
        payment_info=payment_info,
        preferences=preferences
    )

    print(f"Full Name: {person.personal_info.get_full_name()}")
    print(f"Age: {person.personal_info.get_age()}")
    print(f"Address: {person.address.get_full_address()}")
    print(f"Masked Data: {person.mask_sensitive_data()}")