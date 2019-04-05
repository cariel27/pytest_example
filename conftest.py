import pytest
from pytest import Item
import ast
from lib import framework_helper as fr
from lib import util
from lib import config_reader

# ======================================================================================================================

# CUSTOM REPORTER
tests_list = []
PYTEST_INI_PATH = "pytest_tests/pytest.ini"
MARKERS_TO_RUN = ("Working",)
MARKERS_TO_SKIP = ("NotImplementedYet", "Broken", "OutOfScope")
MARKERS_PROCESS_TAG = []

# pytest_config = config_reader.read_config_file(PYTEST_INI_PATH)
# browser_list = pytest_config["pytest"]["browser_config_list"].replace(" ", "").split(",")
# markers_to_run = pytest_config["pytest"]["markers_to_run"].split(",")
# markers_to_skip = pytest_config["pytest"]["markers_to_skip"].split(",")
# markers_process_tag = pytest_config["pytest"]["markers_process_tag"].split(",")

mark_counter = {}

# mark_counter example
# mark_counter = {'Working':
#                     {'total': 0,
#                      'tests': []},
#                 'NotImplementedYet':
#                     {'total': 0,
#                      'tests': []},
#                 'Broken':
#                     {'total': 0,
#                      'tests': []},
#                 }

wrong_marked_tests = {}
# wrong_marked_tests example
# wrong_marked_tests = {'test_name': ['Working', 'NotImplementedYet']}

unmarked_tests = []


def initialize_mark_counter(mark_list: tuple):
    """Initialize mark_counter like a dict"""
    if not mark_counter:
        for mark in mark_list:
            mark_counter[mark] = {}
            mark_counter[mark]['total'] = 0
            mark_counter[mark]['tests'] = []


def process_test_marks(test_item: dict, item_id: str):
    def add_wrong_test_marked(test_item: dict):
        """Add test info to wrong_marked_tests"""

        wrong_marked_tests[item_id] = {}
        wrong_marked_tests[item_id]['Marks'] = test_item[item_id]["test_process_marks"]

    def sum_test_to_mark_counter(test_item: dict):
        """Add test info to mark_counter"""

        for mark in test_item[item_id]["test_process_marks"]:
            mark_counter[mark]['total'] += 1
            mark_counter[mark]['tests'].append(item_id)

    initialize_mark_counter(mark_list=MARKERS_TO_RUN + MARKERS_TO_SKIP)
    process_marks = test_item[item_id]["test_process_marks"]
    test_marks = test_item[item_id]["test_marks"]

    # Process Marks
    if not process_marks:
        unmarked_tests.append(item_id)
        pytest.skip(msg="Test not marked with any Process Marks. Skipped.")
    elif len(process_marks) >= 2:
        add_wrong_test_marked(test_item=test_item)
        pytest.skip(msg="Test contains two or more Process Marks. Skipped.")
    elif process_marks:
        if process_marks[0] not in MARKERS_TO_RUN + MARKERS_TO_SKIP:
            add_wrong_test_marked(test_item=test_item)
            pytest.skip(msg="Mark not recognized: " + process_marks[0] + "'. Skipped")
        else:
            sum_test_to_mark_counter(test_item=test_item)

        if process_marks[0] not in MARKERS_TO_RUN:
            pytest.skip(msg=process_marks[0] + "'. Skipped")


def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption('--mark-metrics', action='store_true', dest='mark metrics')


def pytest_runtest_setup(item: Item):
    # called before pytest_runtest_call(item).

    def get_my_custom_marks(item: Item):
        """:return list with the marks of the test that are included in marks_to_run or marks_to_skip """
        marks = []
        for mark in item.own_markers:
            if mark.name not in MARKERS_PROCESS_TAG:
                marks.append(mark.name)
        return marks

    def get_test_item(item: Item):
        test_dict = {}
        node_id = item.nodeid
        process_tag = []
        is_process_tag = False

        for marker in item.iter_markers(name="test_process_marks"):
            process_tag.append(marker.args[0])
            is_process_tag = True

        if not is_process_tag:
            is_process_tag = False

        other_marks = get_my_custom_marks(item)
        test_dict.update({node_id:
                              {"test_process_marks": process_tag,
                               "is_process_tag": is_process_tag,
                               "test_marks": other_marks,
                               "test_name": item.name}})

        return test_dict

    test_item = get_test_item(item=item)
    item_id = list(test_item.keys())[0]

    tests_list.append(item_id)

    process_test_marks(test_item=test_item, item_id=item_id)


def pytest_sessionfinish(session, exitstatus):
    print_report()


def print_report():
    print('')
    print('\33[2;36;40m'+ '-------------------------------------------------------------------------')
    print('Total: {}'.format(len(tests_list)))
    print('\33[2;36;40m' + '-------------------------------------------------------------------------')

    # Print marked tests
    for mark_name in mark_counter.keys():
        if mark_name in MARKERS_TO_RUN:
            colour = '\033[0;32;40m'
        elif mark_name in MARKERS_TO_SKIP:
            colour = '\033[1;33;40m'
        else:
            colour = '\033[0;35;40m'
        print('{}{}: {}'.format(colour, mark_name, mark_counter[mark_name]['total']))
        print('     Tests: ')

        for test in mark_counter[mark_name]['tests']:
            print('         - {}'.format(test))
    print('\33[2;36;40m' + '-------------------------------------------------------------------------')

    # Print wrongly marked tests
    print('\33[2;31;40m' + 'Wrongly marked tests: {}'.format(len(wrong_marked_tests)))
    for test_name in wrong_marked_tests.keys():
        print('     - {}:'.format(test_name))
        for mark in wrong_marked_tests[test_name]['Marks']:
            print('         - {}'.format(mark))
    print('\33[2;36;40m' + '-------------------------------------------------------------------------')

    # Print unmarked tests
    print('\33[2;31;40m' + 'Unmarked tests: {}'.format(len(unmarked_tests)))
    for test in unmarked_tests:
        print('     - {}'.format(test))
    print('\33[2;36;40m' + '-------------------------------------------------------------------------')
    print('\033[0;37;40m \n')


# ======================================================================================================================


@pytest.fixture(scope="module")
def setup_test_execution(request):
    import platform

    # Now the default environment is REDMINE
    pytest_init_path = "pytest_tests/pytest.ini"
    pytest_config = config_reader.read_config_file(pytest_init_path)
    sut_url = pytest_config.get('pytest.environment.local').get('sut_url')
    env_name = pytest_config.get('pytest.environment.local').get('env_name')
    screenshot_path = pytest_config.get('pytest').get('screenshot_path', None)

    project_root = util.get_project_root_path()

    execution_data = dict({
        "sut_url": sut_url,
        "config_file": pytest_config,
        "environment": env_name,
        "project_root": project_root,
        "platform": platform.system().lower(),
        "driver": None,
        "video_recording": None,
        "run_id": None,
        "date_run": util.get_time_stamp(),
        "test_name": None,
        "scenario_name": None,
        "scenario_passed": None,
        "window_size": None,
        "image_output_path": None,
        "screenshot_path": screenshot_path,
        "screenshot_file_name": None,
        "rest": {},
        "appium_server_url": None,
        "appium_subprocess": [],
        "test_attachment": {"screenshot_path": None}
    })

    pytest.execution_data = execution_data


@pytest.fixture()
def setup_test(get_web_driver):
    yield
    if pytest.execution_data["driver"]:
        if ast.literal_eval(pytest.execution_data["config_file"]["pytest.userdata"]["screenshot"]):
            take_scenario_screenshot()

        close_driver()

    if ast.literal_eval(pytest.execution_data["config_file"]["pytest"].get("use_allure", False)):
        attach_files()


@pytest.fixture()
def get_web_driver(config_iterator):
    browser_config = config_iterator
    is_grid = ast.literal_eval(pytest.execution_data["config_file"]["pytest.userdata"].get("run_on_grid", False))

    if is_grid:
        grid_server_url = pytest.execution_data["config_file"]["pytest.userdata"].get("grid_server_url", None)
    else:
        grid_server_url = None

    driver = fr.setup_desktop_browser(execution_data=pytest.execution_data, config_name=browser_config,
                                      is_grid=is_grid, grid_server_url=grid_server_url)

    # Check if Webdriver was correctly initialized. If not, skip test.
    if driver is None:
        pytest.skip(msg="Exception during browser initialization.")

    pytest.execution_data["driver"] = driver
    pytest.execution_data["window_size"] = driver.get_window_size()

    return driver


def get_browser_list():
    pytest_config = config_reader.read_config_file(PYTEST_INI_PATH)
    browser_list = pytest_config["pytest"]["browser_config_list"].replace(" ", "").split(",")

    return browser_list


@pytest.yield_fixture(scope='session', params=get_browser_list())
def config_iterator(request):
    yield request.param


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport():
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    if hasattr(pytest, "execution_data"):
        if rep.skipped:
            pytest.execution_data["scenario_status"] = "skipped"
        else:
            pytest.execution_data["scenario_status"] = "passed" if rep.passed else "failed"

        pytest.execution_data["test_name"] = rep.location[2].replace("TestClass.", "").split("[")[0]
        pytest.execution_data["scenario_name"] = rep.location[2].replace("TestClass.", "").split("[")[1].replace("]",
                                                                                                                 "")


def take_scenario_screenshot():
    scenario_passed = pytest.execution_data["scenario_status"]
    scenario_name = util.remove_special_characters(string_to_clean=pytest.execution_data["scenario_name"][:60],
                                                   str_exceptions=[".", "-", "_"])

    test_name = pytest.execution_data["test_name"]
    screenshot_path = pytest.execution_data["screenshot_path"]
    date_run = pytest.execution_data["date_run"]

    screenshot_path = util.get_screenshot_path(scenario_status=scenario_passed, scenario_name=scenario_name,
                                               feature_name=test_name, screenshot_path=screenshot_path,
                                               date_run=date_run)

    pytest.execution_data["test_attachment"]["screenshot_path"] = screenshot_path
    pytest.execution_data["test_attachment"]["screenshot_file_name"] = scenario_name + "-" + date_run + '.png'

    util.take_screenshot(driver=pytest.execution_data["driver"], screenshot_path=screenshot_path)


def close_driver():
    if pytest.execution_data["driver"]:
        if ast.literal_eval(pytest.execution_data["config_file"]["pytest.userdata"]["screenshot"]):
            take_scenario_screenshot()
        pytest.execution_data["driver"].close()
        pytest.execution_data["driver"].quit()


def attach_files():
    import allure
    if pytest.execution_data["test_attachment"].get("screenshot_path", False):
        screenshot_name = pytest.execution_data["test_attachment"]["screenshot_file_name"]
        allure.attach.file(source=pytest.execution_data["project_root"] + "/" +
                                  pytest.execution_data["test_attachment"]["screenshot_path"],
                           name=screenshot_name, attachment_type=allure.attachment_type.PNG)
