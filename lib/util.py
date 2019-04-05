import time
from pathlib import Path
from arrow import arrow
from lib.mock_data import Generator
import platform
import sys
import subprocess
import base64
import distro

# LIBRARY LIST
COMMON_LIBRARIES = {"java": "java -version | head -1",
                    "node": "node --version",
                    "npm": "npm --version",
                    "appium": "npm view appium grep version",
                    "git": "brew info git | head -1",
                    "git-lfs": "brew info git-lfs | head -1"}
MAC_LIBRARIES = {"python": "python3 --version",
                 "libimobiledevice": "brew info libimobiledevice | head -1",
                 "ios-webkit-debug-proxy": "brew info ios-webkit-debug-proxy | head -1",
                 "ios-deploy": "npm list ios-deploy"}
WIN_LIBRARIES = {"python": "python --version"}


def remove_special_characters(string_to_clean: str, str_exceptions: list=None) -> str:
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


def read_json_file(file_path):
    import json
    try:
        with open(file_path, "r") as file:
            file = json.load(file)
    except FileNotFoundError as e:
        raise Exception(
            4 * "<" + "[ERROR]" + 4 * ">" + "An error occurred when trying to read  "
            + file_path
            + " file"
            + "\nERROR: "
            + format(e)
            + "\n")
    return file


def call_command_line(command_string: str, options_list=None):
    if options_list is not None:
        options_list.insert(0, command_string)
        command_args = " ".join(options_list)

        # p = call(command_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print("[SUB-PROCESS] " + command_args)
        p = subprocess.Popen(command_args, shell=True)
        sub_process_info = [command_string, options_list[1::], p]
        return sub_process_info

    else:
        process = subprocess.Popen(command_string, shell=True, stderr=subprocess.STDOUT)
        output, error = process.communicate()


# <<<<<<<<<<<<<<<<<DATA CONVERTION>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def validate_list_content(expected_values: list, result_values: list) -> dict:
    """
    Check if two lists has exactly the same content. Compares the expected_values list with the result_values list.
    :param expected_values: a list of expected values willing to be found in result_values.
    :param result_values: The list to be compared to.
    :return: Return a result dictionary with:
    # are_equal: True if both lists have exactly the same values. False otherwise.
    # missing_values: a list of missing values from expected_values list not found in result_values list.
    # unexpected_values: a list of values found in result_values list that are not in expected_values
    """

    result = {"are_equal": True, "missing_values": [], "unexpected_values": []}

    if not expected_values:
        raise Exception(
            4 * "<" + "[ERROR]" + 4 * ">" +
            "Expected Test Test Data cannot have leght = 0"
            "\n")

    # Empty Error List
    if not result_values:
        result["are_equal"] = False
        result["missing_values"] = expected_values

        return result

    # Missing Loop
    for expected in expected_values:
        if not (expected in result_values):
            result["are_equal"] = False
            result["missing_values"].append(expected)

    # Unexpected Loop
    for response_err in result_values:
        if not (response_err in expected_values):
            result["are_equal"] = False
            result["unexpected_values"].append(response_err)

    return result


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


def convert_string_to_float(str_value, num_of_decimals=2):
    """
    Convert Money values like $1000.0 to 1000.0 as float
    :param str_value: value to be c
    :param num_of_decimals: Number of decimals required.
    :return: float value with the accuracy required.
    """
    float_value = str_value.replace("$", "")

    if num_of_decimals == 0:
        float_value = "{0:.0f}".format((float(float_value.replace(',', ''))))
    elif num_of_decimals == 1:
        float_value = "{0:.1f}".format((float(float_value.replace(',', ''))))
    elif num_of_decimals == 2:
        float_value = "{0:.2f}".format((float(float_value.replace(',', ''))))
    elif num_of_decimals == 3:
        float_value = "{0:.3f}".format((float(float_value.replace(',', ''))))

    return float(float_value)


def convert_empty_values_to_string(value):
    """
    Convert "" empty string values to "0"
    :param value: Value to be checked
    :return: 0 if value == "" or value instead.
    """
    if value in ["", " "]:
        return "0"
    else:
        return value


def get_numbers_from_string(str_var):
    """
    Cleans a numeric string like $30,000.00 to 30000.00
    :param str_var:
    :return:
    """
    result = ""
    for s in str_var:
        if s.isdigit() or s == ",":
            result = result + s
        else:
            continue
    return result


def is_field_in_blank(self, web_element):
    """
    Verifies if a field is in blank or is 0
    :param self:
    :param web_element:
    :return:
    """
    text = self.web_element_text(web_element)
    text = text.replace(".", "")

    if text.isdigit():
        float_var = float(text)
        print("float_var: ", float_var)

        if float_var == 0:
            return True

    elif text == "":
        return True

    else:
        return False


# <<<<<<<<<<<<<<<<<DATA CONVERSION/VERIFICATION>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<END>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# <<<<<<<<<<<<<<<<<TIME CONVERSION>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# TODO: Check
def get_time(occurrence=None):
    """
    Get date or/and time depending on occurrence parameter
    :param occurrence: Part of the date time you want to get.
    :return:
    """
    import datetime

    if occurrence is None or occurrence == "today":
        """Returns today's date and time"""
        current_time = datetime.datetime.now().time()
        hour, minutes, seconds = str(current_time).split(":")
        seconds = seconds.split(".")[0]
        return hour + ":" + minutes + ":" + seconds
    elif occurrence.lower() == "month":
        """Returns today's month name"""
        month = datetime.datetime.now().month
        return month
    # TODO: Find the way to get the month Name
    # elif occurrence.lower() == "month_name":
    #     month_name = datetime.datetime.now()
    #     return month_name
    elif occurrence.lower() == "month_number":
        """Returns today's month"""
        month_number = datetime.datetime.now().month
        return month_number
    elif occurrence.lower() == "year":
        """Returns today's year"""
        year = datetime.datetime.now().year
        return year


def get_time_stamp():
    """
    Returns time stamp
    :return: Time stamp format mdY-HMS
    """
    timestr = time.strftime("%m%d%Y-%H%M%S")
    time_stamp = ""
    for i, t in enumerate(timestr):
        if i == 2 or i == 4:
            time_stamp = time_stamp + "-"
        time_stamp = time_stamp + t
    return time_stamp


def seconds_to_hh_mm_ss(seconds):
    """
    Converts seconds to hours/minutes/seconds
    :param seconds:
    :return: [hours, minutes, seconds]
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return h, m, s


# TODO: Check
def compare_two_dates(date_1, date_2, operator=">"):
    """ CHANGE TO GE, GT, LT, LE, etc convention """
    from datetime import datetime
    date_1 = date_1.replace("/", "-")
    date_2 = date_2.replace("/", "-")
    mm, dd, yyyy = date_1.split("-")
    d1 = datetime(int(yyyy), int(mm), int(dd))
    mm, dd, yyyy = date_2.split("-")
    d2 = datetime(int(yyyy), int(mm), int(dd))

    if operator == ">=":
        if d1 >= d2:
            return True
        else:
            return False
    if operator == "<=":
        if d1 <= d2:
            return True
        else:
            return False
    elif operator == ">":
        if d1 > d2:
            return True
        else:
            return False
    elif operator == "<":
        if d1 < d2:
            return True
        else:
            return False


# TODO: Check
def sum_dates(date_1, date_2):
    """
    Sums two dates
    :param date_1: first date to be sum
    :param date_2: second date in format of year or months. eg. 2 years
    :return: The sum of a date plus a year or a month.
    """
    date_1 = date_1.replace("/", "-")
    if date_2.endswith("year") or date_2.endswith("years"):
        date_2.replace("year", "").replace(" ", "")
        mm, dd, yyyy = date_1.split("-")
        result_date = arrow.get(yyyy + "-" + mm + "-" + dd).replace(year=int(date_2)).format(
            'MM/DD/YYYY')
        return result_date
    elif date_2.endswith("month") or date_2.endswith("months"):
        if date_2.endswith("months"):
            date_2 = date_2.replace("months", "").replace(" ", "")
        if date_2.endswith("month"):
            date_2 = date_2.replace("month", "").replace(" ", "")
        mm, dd, yyyy = date_1.split("-")
        result_date = arrow.get(yyyy + "-" + mm + "-" + dd).replace(months=int(date_2)).format('MM/DD/YYYY')
        return result_date


# TODO: Check
def get_dob_by_age(age, reference_date):
    """
    Calculates the dob based on a specific DATE and AGE
    :param age: The standard age
    :param reference_date:
    :return: date of birth according to the age.
    """
    date = reference_date.replace("/", "-")
    mm, dd, yyyy = date.split("-")
    dob = arrow.get(yyyy + "-" + mm + "-" + dd).replace(years=int(-age)).format('MM/DD/YYYY')

    return dob


# <<<<<<<<<<<<<<<<<TIME CONVERSION>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<END>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<DATA GENERATION>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def get_address(by, criteria):
    """
    Get address according to the city, state or zip_code.
    :param by: Address from city, state or zip code.
    :param criteria: could be a zip code number, state or city name.
    :return: Returns a dictionary with the person data generated
    """
    g = Generator()
    if by == "city":
        return g.get_person_by_city(criteria).__as_dict()
    elif by == "state":
        return g.get_person_by_state(criteria).__as_dict()
    elif by == "zip_code":
        return g.get_person_by_zip_code(criteria).__as_dict()


# <<<<<<<<<<<<<<<<<DATA GENERATION>>>>>>>>>>>>>>>>>>>>>>>>>
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

    from assertpy import assert_warn

    if not driver:
        assert_warn(driver,
                    4 * "!" + "[Warning]" + 4 * "!" +
                    "Driver is None. No screenshot was taken.").is_not_none()

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

# <<<<<<<<<<<<<<<<<PRINTING>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def print_feature_duration(feature_name, duration_in_hh_mm_ss):
    print("\n" + 50 * "*")
    print("Feature: " + feature_name)
    print("Time: " + "%d:%02d:%02d" % (duration_in_hh_mm_ss[0], duration_in_hh_mm_ss[1], duration_in_hh_mm_ss[2]))
    print("\n" + 50 * "*")


def print_platform_description():
    def print_generic_description():
        print("""Python version: %s
            system: %s
            platform: %s,
            processor: %s
            """ % (
            sys.version.split('\n'),
            platform.system(),
            platform.version(),
            platform.processor()
        ))

    def print_linux_description():
        print("""Distribution: %s
               """ % (
            distro.linux_distribution()
        ))

    def print_mac_os_description():
        print("""Mac Ver: %s
                       """ % (
            platform.mac_ver()
        ))

    print(50 * "<" + "PLATFORM INFORMATION" + 50 * ">")
    print_generic_description()
    if platform.system().lower() == "linux":
        print_linux_description()


def print_libraries_versions():
    for k in COMMON_LIBRARIES:
        print(60 * "<" + 60 * ">")
        print(k.upper())
        call_command_line(COMMON_LIBRARIES.get(k))

    if platform.system().lower() == "darwin":
        for k in MAC_LIBRARIES:
            print(60 * "<" + 60 * ">")
            print(k.upper())
            call_command_line(MAC_LIBRARIES.get(k))

    if platform.system().lower() == "windows":
        for k in WIN_LIBRARIES:
            print(60 * "<" + 60 * ">")
            print(k.upper())
            call_command_line(WIN_LIBRARIES.get(k))
    if platform.system().lower() == "linux":
        pass

    print(60 * "<" + 60 * ">")
    print("\n")


# <<<<<<<<<<<<<<<<<PRINTING>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<END>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<GIT>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def get_current_branch_name(repo_path=None):
    """
    Returns the name of the active Git branch as a string.
    :param repo_path:
    :return: Current Branch name as String
    """
    from git import Repo

    # By default gets proyect repo path.
    if repo_path is None:
        repo_path = get_project_root_path()

    repo = Repo(repo_path)
    try:
        branch = repo.active_branch
        branch_name = branch.name
    except Exception as e:
        print(
            4 * "<" + "[WARNING]" + 4 * ">" + "Not able to get branch name."
            + " file"
            + "\nERROR: "
            + format(e)
            + "\n")
        branch_name = None
    finally:
        repo.close()

    return branch_name


def get_revision_number(repo_path=None):
    """
    Returns the revision name of the active Git branch as a string.
    :param repo_path:
    :return:
    """

    repo = __get_repo_instance(repo_path)

    branch = repo.active_branch
    return branch.commit.name_rev


def get_revision_last_commit_date_time(repo_path=None):
    """
    Returns the datetime of the last commit of the active Git branch as a string.
    :param repo_path:
    :return:
    """
    repo = __get_repo_instance(repo_path)
    branch = repo.active_branch
    return branch.commit.committed_datetime


def __get_repo_instance(repo_path):
    from git import Repo

    # By default gets proyect repo path.
    if repo_path is None:
        repo_path = get_project_root_path()

    return Repo(repo_path)


# <<<<<<<<<<<<<<<<<GIT>>>>>>>>>>>>>>>>>>>>>>>>>
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


def delete_folder(folder_path):
    """
    Delete a folder. If it is not empty, checks the 2nd level. Delete inner folders without checking if they are empty
    or not. Is not a recursive method.
    :param folder_path: Folder path to be deleted
    :return:
    """
    import os

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        if len(os.listdir(folder_path)) == 0:
            os.rmdir(folder_path)
        else:
            for d in os.listdir(folder_path):
                os.rmdir(folder_path + "/" + d)

        os.rmdir(folder_path)
    # else:
    #     print(folder_path + " does NOT exist or is NOT a folder.")


def get_file_names_from_path(target_path):
    """
    Return file names in the target_path.
    :param target_path: Relative to project target path. eg. report/screenshots
    :return: File names in path
    """

    import os

    head = get_project_root_path()
    # Absolute path to report files
    report_path = head + "/" + target_path
    report_path = convert_slash_path(report_path)
    # Files allocated on report path
    files_in_path = os.listdir(report_path)

    return files_in_path


# <<<<<<<<<<<<<<<<<FILES>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<END>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# <<<<<<<<<<<<<<<<<IMAGE>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def get_standard_img_path(context) -> str:
    """
    Returns the standard image path for Image Based Testing based on project root path and the image path passed as
    parameter in Step Data Table.
    :param context:
    :return: Image path
    """
    path = context.execution_data["project_root"] + context.td["standard_image_path"]

    return path


def get_full_image_output_path(execution_data: dict) -> str:
    """
        Returns the full image path for Image Based Testing. It has the following format:
        image_output_path/feature_name_scenario_name_SCREENSHOT_timestamp.png

        where:  image_output_path is the output path defined in behave.ini config file.
                feature_name is the current feature name taken from the context.feature.
                scenario name is the current scenario name taken from the context.scenario.
        :param execution_data:
        :return: Image path
    """
    path = execution_data["image_output_path"] + execution_data["feature_name"] + "_" + execution_data[
        "scenario_name"] + "_SCREENSHOT_" + execution_data["date_run"] + ".png"

    return path


def get_result_image_output_path(execution_data: dict, validation_name: str) -> str:
    """
       Returns the result image output path for Image Based Testing. It has the following format:
       image_output_path/feature_name_scenario_name_VALIDATION_RESULT_validation_name_timestamp.png

       where:  image_output_path is the output path defined in behave.ini config file.
               feature_name is the current feature name taken from the context.feature.
               scenario name is the current scenario name taken from the context.scenario.
       :param execution_data:
       :param validation_name: Validation name to be appended to the image
       :return: Image path
       """
    path = execution_data["image_output_path"] + execution_data["feature_name"] + "_" + execution_data[
        "scenario_name"] + "_VALIDATION_RESULT_" + validation_name + "_" + execution_data["date_run"] + ".png"

    return path


def get_base64_by_image_path(image_path: str):
    with open(image_path, 'rb') as png_file:
        base64_data = get_base64_image(png_file)

    return base64_data


def get_base64_image(image_file):
    return base64.b64encode(image_file.read()).decode('UTF-8')


def decode_base64(coded_string: str):
    return base64.b64decode(coded_string)

# <<<<<<<<<<<<<<<<<IMAGE>>>>>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>
