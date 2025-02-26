from abc import ABC, abstractmethod
from datetime import datetime


# Observer Interface
class Observer(ABC):
    @abstractmethod
    def update(self, subject, property_name, old_value, new_value):
        pass


# Observable (Subject) Class
class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, property_name, old_value, new_value):
        print(f"📢 Notifying {len(self._observers)} observers about change in {property_name}")
        for observer in self._observers:
            observer.update(self, property_name, old_value, new_value)


# System that implements Observable
class TemperatureMonitor(Observable):
    def __init__(self):
        super().__init__()
        self._temperature = 25  # Initial temperature in degrees Celsius

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if value == self._temperature:
            return  # No change, no notification

        print(f"🌡️ Changing temperature from {self._temperature}°C to {value}°C")
        old_value = self._temperature
        self._temperature = value
        self.notify_observers("temperature", old_value, self._temperature)


# Concrete Observers
class TemperatureDisplay(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, subject, property_name, old_value, new_value):
        print(f"📱 {self.name}: Temperature has changed from {old_value}°C to {new_value}°C!")


class TemperatureLogger(Observer):
    def update(self, subject, property_name, old_value, new_value):
        print(f'📝 LOG: Temperature updated to {new_value}°C at {datetime.now().strftime("%H:%M:%S")}')


class TemperatureAlarm(Observer):
    def __init__(self, threshold=30):
        self.threshold = threshold

    def update(self, subject, property_name, old_value, new_value):
        if new_value > self.threshold:
            print(f"🔔 ALARM! Critical temperature: {new_value}°C exceeds threshold of {self.threshold}°C")
        else:
            print(f"✅ Temperature {new_value}°C is within normal range")


# Usage example
def run_demo():
    # Create the temperature monitor
    thermometer = TemperatureMonitor()

    # Create observers
    display1 = TemperatureDisplay("Living Room Screen")
    display2 = TemperatureDisplay("Kitchen Screen")
    logger = TemperatureLogger()
    alarm = TemperatureAlarm(threshold=30)

    # Subscribe observers
    print("👥 Subscribing observers to the temperature monitor")
    thermometer.add_observer(display1)
    thermometer.add_observer(display2)
    thermometer.add_observer(logger)
    thermometer.add_observer(alarm)
    print(f"✅ Total observers: {len(thermometer._observers)}")

    # Change temperature and see notifications
    print("\n--- First temperature change ---")
    thermometer.temperature = 28

    print("\n--- Second temperature change (exceeds threshold) ---")
    thermometer.temperature = 32

    print("\n--- Removing an observer ---")
    thermometer.remove_observer(display2)
    print(f"✅ Remaining observers: {len(thermometer._observers)}")

    print("\n--- Temperature change after removing an observer ---")
    thermometer.temperature = 29


# Run demonstration
if __name__ == "__main__":
    run_demo()
