from lib import config_reader as cfg_reader
from lib.browser_factory import BrowserFactory as Bf


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
