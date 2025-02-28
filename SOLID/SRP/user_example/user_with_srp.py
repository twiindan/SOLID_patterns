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


# APPLYING SRP: Splitting into multiple classes, each with a single responsibility
# This class is only responsible for handling personal information
@dataclass
class PersonalInfo:
    first_name: str
    last_name: str
    birth_date: date
    gender: Gender
    nationality: str
    tax_id: str
    social_security_number: str

    # Methods related only to personal information
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_age(self) -> int:
        today = date.today()
        return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day))


# APPLYING SRP: Class dedicated to managing contact information
@dataclass
class ContactInfo:
    email: str
    phone_number: str
    alternative_phone: Optional[str] = None

    # Methods related only to contact information
    def mask_email(self) -> str:
        return f"{self.email[:3]}...@{self.email.split('@')[1]}"

    def mask_phone(self) -> str:
        return f"***{self.phone_number[-4:]}"


# APPLYING SRP: Class dedicated to address handling
@dataclass
class Address:
    street: str
    street_number: str
    city: str
    state: str
    postal_code: str
    country: str
    apartment: Optional[str] = None

    # Method related only to address formatting
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


# APPLYING SRP: Class dedicated to credit card information
@dataclass
class CardInfo:
    card_number: str
    card_holder_name: str
    card_expiry_month: int
    card_expiry_year: int
    card_cvv: str

    # Methods related only to card operations
    def mask_card_number(self) -> str:
        return f"****-****-****-{self.card_number[-4:]}"

    def is_expired(self) -> bool:
        today = date.today()
        return (today.year > self.card_expiry_year or
                (today.year == self.card_expiry_year and
                 today.month > self.card_expiry_month))


# APPLYING SRP: Class dedicated to bank account information
@dataclass
class BankInfo:
    bank_name: str
    account_number: str
    routing_number: str
    swift_code: Optional[str] = None
    iban: Optional[str] = None

    # Method related only to bank information
    def mask_account_number(self) -> str:
        return f"****{self.account_number[-4:]}"


# APPLYING SRP: Class to handle payment-related information
@dataclass
class PaymentInfo:
    payment_method: PaymentMethod
    card_info: Optional[CardInfo] = None
    bank_info: Optional[BankInfo] = None


# APPLYING SRP: Class to handle user preferences
@dataclass
class Preferences:
    preferred_language: str = "en"
    marketing_consent: bool = False
    newsletter_subscription: bool = False


# APPLYING SRP: Main Person class now acts as a composite of the specialized classes
# Each attribute is a well-defined object with its own responsibility
@dataclass
class Person:
    id: str
    personal_info: PersonalInfo  # Delegating personal information responsibility
    contact_info: ContactInfo  # Delegating contact information responsibility
    address: Address  # Delegating address responsibility
    payment_info: PaymentInfo  # Delegating payment information responsibility
    preferences: Preferences  # Delegating preferences responsibility
    billing_address: Optional[Address] = None
    created_at: date = field(default_factory=date.today)
    updated_at: date = field(default_factory=date.today)
    is_active: bool = True

    # This method now delegates to the appropriate objects instead of handling the logic itself
    def mask_sensitive_data(self) -> dict:
        """Returns a version of the data with sensitive information masked"""
        masked_data = {
            "id": self.id,
            "name": self.personal_info.get_full_name(),  # Delegating to PersonalInfo
            "email": self.contact_info.mask_email(),  # Delegating to ContactInfo
            "phone": self.contact_info.mask_phone(),  # Delegating to ContactInfo
        }

        if self.payment_info.card_info:
            masked_data["card_number"] = self.payment_info.card_info.mask_card_number()  # Delegating to CardInfo

        if self.payment_info.bank_info:
            masked_data["bank_account"] = self.payment_info.bank_info.mask_account_number()  # Delegating to BankInfo

        return masked_data


# Example to use
if __name__ == "__main__":
    # Note how initialization is now more organized and each component is created separately
    # This makes the code more maintainable and easier to test

    # Creating personal information component
    personal_info = PersonalInfo(
        first_name="John",
        last_name="Doe",
        birth_date=date(1990, 1, 15),
        gender=Gender.MALE,
        nationality="US",
        tax_id="123-45-6789",
        social_security_number="987-65-4321"
    )

    # Creating contact information component
    contact_info = ContactInfo(
        email="john.doe@example.com",
        phone_number="+1234567890"
    )

    # Creating address component
    address = Address(
        street="Main Street",
        street_number="123",
        city="New York",
        state="NY",
        postal_code="10001",
        country="United States"
    )

    # Creating card information component
    card_info = CardInfo(
        card_number="4111111111111111",
        card_holder_name="John Doe",
        card_expiry_month=12,
        card_expiry_year=2025,
        card_cvv="123"
    )

    # Creating payment information component
    payment_info = PaymentInfo(
        payment_method=PaymentMethod.CREDIT_CARD,
        card_info=card_info
    )

    # Creating preferences component
    preferences = Preferences()

    # Assembling the complete Person object from its components
    person = Person(
        id="P12345",
        personal_info=personal_info,
        contact_info=contact_info,
        address=address,
        payment_info=payment_info,
        preferences=preferences
    )

    # Note how method calls are more intuitive and follow a logical path
    print(f"Full Name: {person.personal_info.get_full_name()}")
    print(f"Age: {person.personal_info.get_age()}")
    print(f"Address: {person.address.get_full_address()}")
    print(f"Masked Data: {person.mask_sensitive_data()}")

"""
With SRP:

Responsibilities are split across multiple specialized classes
Each class has a single, well-defined purpose
Methods are located in the classes most appropriate for their functionality
Code is more maintainable and easier to test
Changes to one aspect (e.g., payment processing) won't affect other aspects
Object creation is more organized and follows a clear component-based structure
"""