from another_module import another_module_loading_configuration
from configuration import Configuration

print('Im the first module')
configuration = Configuration()
configuration.load_configuration()
print(configuration.get_browser())

another_module_loading_configuration()
