from lib import util
import os
import configparser

head, tail = os.path.split(os.path.dirname(os.path.abspath(__file__)))
head += "/"
behave_ini_path = head + "/behave.ini"


def read_config_file(ini_path):
    """
    Reads the ini config file.
    :ini_path: is the path of the file.
    :param ini_path: .ini file path
    :return: Dictionary with section:option keys/values.
    """
    config_file = configparser.RawConfigParser()
    config_file.optionxform = str
    config_file.read(ini_path)

    # Create dict for config file information.
    config_info = {}

    # Iterate config file sections.
    for section in config_file.sections():
        config_info[section] = {}

        # Iterate options for each section and append_values into the dict.
        for option in config_file.options(section):
            config_info[section][option] = config_file.get(section, option)

    return config_info


def get_browser_json_config(config_file_name: str):
    webdriver_config_file_path = read_config_file(ini_path=behave_ini_path)["behave"]["webdriver_config_files"]
    json_file_config_path = head + webdriver_config_file_path + config_file_name+".json"
    return get_config(json_file_config_path)


def get_appium_config(config_file_name: str):
    appium_config_file_path = read_config_file(ini_path=behave_ini_path)["behave"]["appium_config_files"]
    json_file_config_path = head + appium_config_file_path + config_file_name + ".json"
    return get_config(json_file_config_path)


def get_report_portal_config():
    report_portal_config_file_path = read_config_file(ini_path=behave_ini_path)["behave"]["report_portal_config_file"]
    file_config_path = head + report_portal_config_file_path
    return read_config_file(file_config_path)


def get_config(config_file_path: str):
    return util.read_json_file(config_file_path)




