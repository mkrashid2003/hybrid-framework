import os
import configparser

# Build a common file path for your configuration file
config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Configuration", "configData.ini")
# Create a parser instance
config_parser = configparser.ConfigParser()
config_parser.read(config_file_path)

class ReadConfig:
    @staticmethod
    def getBaseUrl():
        return config_parser.get("commonData", "base_url")

    @staticmethod
    def getUserName():
        return config_parser.get("commonData", "userName")

    @staticmethod
    def getCommonData(section, key_value):
        # Use the global config_parser that has already read the file
        print("Available sections:", config_parser.sections())  # Debug: see what sections are loaded
        return config_parser.get(section, key_value)
