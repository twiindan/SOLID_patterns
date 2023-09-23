from configuration import Configuration


def another_module_loading_configuration():
    print("I'm the second module")
    configuration = Configuration()
    print(configuration.get_browser())
