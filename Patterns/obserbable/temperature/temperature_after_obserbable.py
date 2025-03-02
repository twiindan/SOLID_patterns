from abc import ABC, abstractmethod
from datetime import datetime


# Observer Interface
# This abstract class defines the contract that all observers must follow
class Observer(ABC):
    @abstractmethod
    def update(self, subject, property_name, old_value, new_value):
        """
        Method called by the Observable when a state change occurs

        Parameters:
        - subject: The Observable object that triggered the update
        - property_name: Name of the property that changed
        - old_value: Previous value before the change
        - new_value: New value after the change
        """
        pass


# Observable (Subject) Class
# This is the base class for objects that need to be observed
# It maintains a list of observers and notifies them of changes
class Observable:
    def __init__(self):
        # List to store all registered observers
        self._observers = []

    def add_observer(self, observer):
        """Register a new observer if not already present"""
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        """Unregister an existing observer"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, property_name, old_value, new_value):
        """Notify all registered observers about a state change"""
        print(f"📢 Notifying {len(self._observers)} observers about change in {property_name}")
        # Loop through all observers and call their update method
        for observer in self._observers:
            observer.update(self, property_name, old_value, new_value)


# Concrete Observable (Subject) implementation
# This class extends Observable to create a specific subject that monitors temperature
class TemperatureMonitor(Observable):
    def __init__(self):
        super().__init__()  # Initialize the parent Observable class
        self._temperature = 25  # Initial temperature in degrees Celsius

    # Property getter - allows access to temperature using object.temperature
    @property
    def temperature(self):
        return self._temperature

    # Property setter - automatically called when temperature is assigned a new value
    # This is where the Observer pattern shines - state changes trigger notifications
    @temperature.setter
    def temperature(self, value):
        # Skip notification if value hasn't changed
        if value == self._temperature:
            return  # No change, no notification

        print(f"🌡️ Changing temperature from {self._temperature}°C to {value}°C")
        old_value = self._temperature
        self._temperature = value
        # Notify all observers about the temperature change
        self.notify_observers("temperature", old_value, self._temperature)


# Concrete Observer #1: Display
# This observer shows the temperature change on a display
class TemperatureDisplay(Observer):
    def __init__(self, name):
        self.name = name  # Each display has a name/location

    def update(self, subject, property_name, old_value, new_value):
        """Implement the Observer interface to display temperature changes"""
        print(f"📱 {self.name}: Temperature has changed from {old_value}°C to {new_value}°C!")


# Concrete Observer #2: Logger
# This observer logs temperature changes with timestamps
class TemperatureLogger(Observer):
    def update(self, subject, property_name, old_value, new_value):
        """Implement the Observer interface to log temperature changes"""
        print(f'📝 LOG: Temperature updated to {new_value}°C at {datetime.now().strftime("%H:%M:%S")}')


# Concrete Observer #3: Alarm
# This observer triggers alarms when temperature exceeds a threshold
class TemperatureAlarm(Observer):
    def __init__(self, threshold=30):
        self.threshold = threshold  # Configurable temperature threshold

    def update(self, subject, property_name, old_value, new_value):
        """Implement the Observer interface to check for temperature threshold violations"""
        if new_value > self.threshold:
            print(f"🔔 ALARM! Critical temperature: {new_value}°C exceeds threshold of {self.threshold}°C")
        else:
            print(f"✅ Temperature {new_value}°C is within normal range")


# Demonstration function to show the Observer pattern in action
def run_demo():
    # Create the temperature monitor (the Observable/Subject)
    thermometer = TemperatureMonitor()

    # Create different types of observers
    display1 = TemperatureDisplay("Living Room Screen")
    display2 = TemperatureDisplay("Kitchen Screen")
    logger = TemperatureLogger()
    alarm = TemperatureAlarm(threshold=30)

    # Register observers with the Observable
    # This is the "subscription" part of the pattern
    print("👥 Subscribing observers to the temperature monitor")
    thermometer.add_observer(display1)
    thermometer.add_observer(display2)
    thermometer.add_observer(logger)
    thermometer.add_observer(alarm)
    print(f"✅ Total observers: {len(thermometer._observers)}")

    # First state change - temperature below threshold
    # This will notify all observers but won't trigger the alarm
    print("\n--- First temperature change ---")
    thermometer.temperature = 28

    # Second state change - temperature above threshold
    # This will notify all observers AND trigger the alarm
    print("\n--- Second temperature change (exceeds threshold) ---")
    thermometer.temperature = 32

    # Demonstrating dynamic observer management
    # We can add/remove observers at runtime - a key benefit of this pattern
    print("\n--- Removing an observer ---")
    thermometer.remove_observer(display2)
    print(f"✅ Remaining observers: {len(thermometer._observers)}")

    # Third state change after removing an observer
    # Only the remaining observers will be notified
    print("\n--- Temperature change after removing an observer ---")
    thermometer.temperature = 29


# Run the demonstration when the script is executed directly
if __name__ == "__main__":
    run_demo()

# KEY BENEFITS OF THE OBSERVER PATTERN SHOWN IN THIS EXAMPLE:
# 1. Loose coupling - the Observable doesn't need to know details about its Observers
# 2. One-to-many relationship - multiple Observers can monitor a single Observable
# 3. Dynamic relationships - Observers can be added/removed at runtime
# 4. Different types of Observers - various classes can respond differently to the same event
# 5. Separation of concerns - temperature monitoring logic is separate from display, logging, and alarm logic
