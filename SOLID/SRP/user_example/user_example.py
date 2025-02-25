from dataclasses import dataclass
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
class Person:
    # Required Data
    id: str
    first_name: str
    last_name: str
    birth_date: date
    gender: Gender
    nationality: str
    tax_id: str
    social_security_number: str
    email: str
    phone_number: str
    street: str
    street_number: str
    city: str
    state: str
    postal_code: str
    country: str
    payment_method: PaymentMethod
    created_at: date
    updated_at: date

    # Optional Data
    alternative_phone: Optional[str] = None
    apartment: Optional[str] = None
    is_billing_address_different: bool = False
    billing_street: Optional[str] = None
    billing_street_number: Optional[str] = None
    billing_apartment: Optional[str] = None
    billing_city: Optional[str] = None
    billing_state: Optional[str] = None
    billing_postal_code: Optional[str] = None
    billing_country: Optional[str] = None
    card_number: Optional[str] = None
    card_expiry_month: Optional[int] = None
    card_expiry_year: Optional[int] = None
    card_cvv: Optional[str] = None
    card_holder_name: Optional[str] = None
    bank_name: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_routing_number: Optional[str] = None
    swift_code: Optional[str] = None
    iban: Optional[str] = None
    preferred_language: str = "en"
    marketing_consent: bool = False
    newsletter_subscription: bool = False
    is_active: bool = True

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_age(self) -> int:
        today = date.today()
        return today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day))

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

    def get_billing_address(self) -> str:
        if not self.is_billing_address_different:
            return self.get_full_address()

        address_parts = [
            self.billing_street,
            self.billing_street_number,
            self.billing_apartment,
            self.billing_postal_code,
            self.billing_city,
            self.billing_state,
            self.billing_country
        ]
        return ", ".join(part for part in address_parts if part)

    def update_payment_method(self, new_method: PaymentMethod) -> None:
        self.payment_method = new_method
        self.updated_at = date.today()

    def mask_sensitive_data(self) -> dict:
        return {
            "id": self.id,
            "name": self.get_full_name(),
            "email": f"{self.email[:3]}...@{self.email.split('@')[1]}",
            "phone": f"***{self.phone_number[-4:]}",
            "card_number": f"****-****-****-{self.card_number[-4:]}" if self.card_number else None,
            "bank_account": f"****{self.bank_account_number[-4:]}" if self.bank_account_number else None
        }


# Example to use
if __name__ == "__main__":
    person = Person(
        id="P12345",
        first_name="John",
        last_name="Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        nationality="US",
        tax_id="123-45-6789",
        social_security_number="987-65-4321",
        email="john.doe@example.com",
        phone_number="+1234567890",
        street="Main Street",
        street_number="123",
        city="New York",
        state="NY",
        postal_code="10001",
        country="United States",
        payment_method=PaymentMethod.CREDIT_CARD,
        created_at=date.today(),
        updated_at=date.today(),
        # Campos opcionales
        card_number="4111111111111111",
        card_expiry_month=12,
        card_expiry_year=2025,
        card_cvv="123",
        card_holder_name="John Doe"
    )

    print(f"Full Name: {person.get_full_name()}")
    print(f"Age: {person.get_age()}")
    print(f"Address: {person.get_full_address()}")
    print(f"Masked Data: {person.mask_sensitive_data()}")