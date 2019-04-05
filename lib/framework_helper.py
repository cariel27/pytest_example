from lib import config_reader as cfg_reader
from lib import appium_helper
from lib import util
from lib.browser_factory import BrowserFactory as Bf
from retry import retry
from appium import webdriver as appium_webdriver

# APPIUM COMMANDS
APPIUM_COMMAND = 'appium'
APPIUM_COMMAND_UDID = '-U'
APPIUM_COMMAND_PORT = '--port'
APPIUM_COMMAND_ADDRESS = '--address'
APPIUM_COMMAND_FULL_RESET = '--full-reset'
APPIUM_COMMAND_DEVICE_NAME = '--device-name'
APPIUM_COMMAND_PLATFORM_NAME = '--platform-name'
APPIUM_COMMAND_PLATFORM_VERSION = '--platform-version'
APPIUM_COMMAND_APP = '--app'
APPIUM_COMMAND_BROWSER_NAME = '--browser-name'
APPIUM_COMMAND_CHROME_DRIVER_PORT = '--chromedriver-port'
APPIUM_SELENDROID_PORT = '--selendroid-port'
APPIUM_SHOW_CONFIG = '--show-config'
APPIUM_NODE_CONFIG = '--nodeconfig'
APPIUM_TMP_DIR = '--tmp'
APPIUM_TRACE_DIR = '--trace-dir'
APPIUM_SUPPRESS_ADB_KILL_SERVER = '--suppress-adb-kill-server'
APPIUM_REBOOT = '--reboot'
APPIUM_WEBKIT_DEBUG_PROXY_PORT = '--webkit-debug-proxy-port'
APPIUM_ISOLATE_SIM_DEVICE = '--isolate-sim-device'
APPIUM_INSTRUMENTS = '--instruments'
APPIUM_DEFAULT_DEVICE = '--default-device'
APPIUM_FORCE_IPHONE = '--force-iphone'
APPIUM_FORCE_IPAD = '--force-ipad'


def setup_appium_driver(execution_data: dict, server_parameters: dict, capabilities: dict, is_grid=False,
                        grid_server_url=None):
    # UiAutomator2 port
    if capabilities.get("automationName", "N/A").lower() == "uiautomator2" and \
            capabilities.get("systemPort", False):
        capabilities["systemPort"] = appium_helper.is_port_available(server_parameters["address"],
                                                                     str(capabilities.get("systemPort")))
        capabilities["systemPort"] = int(capabilities["systemPort"])

    # SELENIUM GRID
    if is_grid:
        if grid_server_url:
            driver = create_appium_webdriver_remote(server_url=grid_server_url, desired_capabilities=capabilities)
        else:
            raise ValueError("Invalid Grid Server URL: {}".format(grid_server_url))

    # LOCAL APPIUM SERVER
    else:
        if not execution_data["appium_subprocess"]:
            execution_data["appium_subprocess"] = start_appium_server(server_parameters)
            execution_data["appium_server_url"] = "http://" + server_parameters[
                "address"] + ":" + appium_available_port + "/wd/hub"

        driver = create_appium_webdriver_remote(server_url=execution_data["appium_server_url"],
                                                desired_capabilities=capabilities)

    return driver


def setup_desktop_browser(execution_data: dict, config_name: str, is_grid=False, grid_server_url=None):
    json_cfg = cfg_reader.get_browser_json_config(config_file_name=config_name)

    # TODO: Move this another part.
    profile_options_dic = json_cfg.get("moz:firefoxOptions", {}).get("prefs", None)

    # LOCAL BROWSER
    if is_grid:
        from selenium import webdriver
        driver = webdriver.Remote(command_executor=grid_server_url, desired_capabilities=json_cfg)

    # REMOTE BROWSER
    else:
        browser_name = json_cfg.get("browserName", None)

        driver = Bf.get_driver(browser_name=browser_name,
                               desired_capabilities=json_cfg,
                               firefox_profile=profile_options_dic,
                               platform=execution_data["platform"])
    return driver


@retry(exceptions=Exception, tries=30, delay=1)
def create_appium_webdriver_remote(server_url: str, desired_capabilities: dict):
    return appium_webdriver.Remote(command_executor=server_url,
                                   desired_capabilities=desired_capabilities)


def start_appium_server(param):
    appium_options = []

    # # Available port for appium
    global appium_available_port
    appium_available_port = appium_helper.is_port_available(param.get("address", "127.0.0.1"), param["port"])

    # Launching Appium Server by CONSOLE COMMANDS:
    # ALL MOBILE PLATFORM
    if param.get("udid", False):
        appium_options.append(APPIUM_COMMAND_UDID)
        appium_options.append(param.get("udid"))
    appium_options.append(APPIUM_COMMAND_PORT)
    appium_options.append(appium_available_port)
    appium_options.append(APPIUM_COMMAND_ADDRESS)
    appium_options.append(param.get("address", "127.0.0.1"))

    if param.get("chromedriver_port", False):
        appium_options.append(APPIUM_COMMAND_CHROME_DRIVER_PORT)
        appium_options.append(param.get("chromedriver_port"))
    if param.get("selendroid_port", False):
        appium_options.append(APPIUM_SELENDROID_PORT)
        appium_options.append(param.get("selendroid_port"))
    if param.get("show_config", False):
        appium_options.append(APPIUM_SHOW_CONFIG)
        appium_options.append(param.get("show_config"))
    if param.get("nodeconfig", False):
        appium_options.append(APPIUM_NODE_CONFIG)
        appium_options.append(param.get("nodeconfig"))
    if param.get("tmp_dir", False):
        appium_options.append(APPIUM_TMP_DIR)
        appium_options.append(param.get("tmp_dir"))
    if param.get("trace_dir", False):
        appium_options.append(APPIUM_TRACE_DIR)
        appium_options.append(param.get("trace_dir"))
    # ANDROID ONLY
    if param.get("suppress_adb_kill_server", False):
        appium_options.append(APPIUM_SUPPRESS_ADB_KILL_SERVER)
        appium_options.append(param.get("suppress_adb_kill_server"))
    if param.get("reboot", False):
        appium_options.append(APPIUM_REBOOT)
        appium_options.append(param.get("reboot"))
    # IOS ONLY
    if param.get("default_device", False):
        appium_options.append(APPIUM_DEFAULT_DEVICE)
        appium_options.append(param.get("default_device"))
    if param.get("instruments", False):
        appium_options.append(APPIUM_INSTRUMENTS)
        appium_options.append(param.get("instruments"))
    if param.get("isolate_sim_device", False):
        appium_options.append(APPIUM_ISOLATE_SIM_DEVICE)
        appium_options.append(param.get("isolate_sim_device"))
    if param.get("webkit_debug_proxy_port", False):
        appium_options.append(APPIUM_WEBKIT_DEBUG_PROXY_PORT)
        appium_options.append(param.get("webkit_debug_proxy_port"))
    if param.get("force_iphone", False):
        appium_options.append(APPIUM_FORCE_IPHONE)
        appium_options.append(param.get("force_iphone"))
    if param.get("force_ipad", False):
        appium_options.append(APPIUM_FORCE_IPAD)
        appium_options.append(param.get("force_ipad"))

    return util.call_command_line(APPIUM_COMMAND, appium_options)
