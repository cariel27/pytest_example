from pathlib import Path


def remove_special_characters(string_to_clean: str, str_exceptions: list = None) -> str:
    return "".join(str for str in string_to_clean if str.isalnum() or str in str_exceptions)


def get_project_root_path():
    return str(Path(__file__).parent.parent)


def get_parameters_from_config_file(config: dict, section: str) -> dict:
    """

    :param config: Config file as dictionary
    :param section: Config file section
    :return: Return a dictionary containing filtered parameters of a configuration dict.
    """
    # Get Global Server Flags from behave.ini file
    parameters = config.get(section)

    # Filtering key/values parameters which don't have values in behave.ini file
    parameters = filter_config_dict(parameters)
    return parameters


def filter_config_dict(var_dict):
    """
    Remove parameters which contains empty values in form of to_be_removed list
    :param var_dict:
    :return: Filtered dictionary without containing parameters with values in to_be_removed list
    """
    to_be_removed = ["", "no", "None"]
    """
    Filter dictionary removing values in to_be_removed list.
    :param var_dict: var dictionary
    :return: Filtered dictionary
    """
    # Filtering key/values parameters which don't have values in behave.ini file
    var_dict_filtered = list()
    # # Getting keys of the parameter which have values distinct than "" (Empty)
    keys = [k for k in var_dict if var_dict[k] not in to_be_removed]
    # # Using the resulting keys to re create the dict
    var_dict_filtered = {k: var_dict[k] for k in keys}

    return var_dict_filtered


def convert_slash_path(f_path):
    """
        Checks platform and performs conversion from windows path to mac & linux ones if needed.
        :param f_path:
        :return:
    """
    import platform

    if platform.system().lower() != "windows":
        f_path = f_path.replace("\\", "/")

    return f_path


# <<<<<<<<<<<<<<<<<DATA CONVERSION/VERIFICATION>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<END>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<WEBELEMENT>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def take_screenshot(driver, screenshot_path: str) -> None:
    """
    Takes a browser screenshot.
    :param driver: Webdriver instance
    :param screenshot_path: Screenshot folder name
    :return: None
    """

    # Save screenshot on specified folder
    try:
        driver.save_screenshot(screenshot_path)
    except Exception as e:
        print(4 * "<" + "[ERROR]" + 4 * ">" + "An error occurred when trying to take a screenshot."
              + "\nERROR: "
              + format(e)
              + "\n")


def get_screenshot_path(scenario_status: str, scenario_name: str, feature_name: str, screenshot_path: str,
                        date_run: str) -> str:
    """
    Get screenshot path according to scenario_status/feature_name/scenario_name_date_run.png
    E.g. The full path would be 'reports/screenshots/
                        passed/DESKTOP_WEBUI_-_REDMINE_-_LOGIN/
                        user_inputs_correct_username_and_password_--_config_chrome_default_config-03-01-2019-124035.png'

    :param scenario_status:
    :param scenario_name:
    :param feature_name:
    :param screenshot_path: screenshot folder in behave.ini
    :param date_run: time stamp
    :return: full screenshot file path where it will be saved.
    """
    # project root from here
    if scenario_status == "passed":
        end_folder = "passed/"
    elif scenario_status == "failed":
        end_folder = "failed/"
    else:
        end_folder = "temp/"
        create_folder(screenshot_path + end_folder)

    # Screenshot folder destiny
    screenshot_folder = convert_slash_path(screenshot_path + end_folder + feature_name + "/")

    create_folder(screenshot_folder)

    # Screenshot filename
    screenshot_file_name = scenario_name + "-" + date_run + '.png'

    return screenshot_folder + screenshot_file_name


def save_web_element_screenshot(web_element, screenshot_path: str):
    try:
        with open(file=screenshot_path, mode="wb") as login_png:
            login_png.write(web_element.screenshot_as_png)
    except Exception as e:
        print(
            4 * "<" + "[ERROR]" + 4 * ">" + "An error occurred when taking web element screenshot."
            + "\nERROR: "
            + format(e)
            + "\n")


# <<<<<<<<<<<<<<<<<WEBELEMENT>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<END>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# <<<<<<<<<<<<<<<<<FILES>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def write_file(file_path: str, data=None, method="a") -> None:
    """
    Writes a file in file_path path.
    :param file_path:
    :param data:
    :param method: By default the method is "append".
    :return: None
    """
    try:
        with open(file_path, method) as f:
            if data is not None:
                f.write(data)
    except FileNotFoundError as e:
        raise Exception("\nFile path provided is incorrect:" + "\nFile path: " + e.filename + "\nError: " + e.strerror)


def create_folder(file_path):
    import os
    import errno

    # Check platform and convert \ to / in file path
    file_path = convert_slash_path(file_path)

    try:
        os.mkdir(file_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise Exception("Error when creating a folder in " + file_path + "\n")
