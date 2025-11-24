import pytest
from playwright.sync_api import sync_playwright, Browser, Page
from PageObjects.Login_Page.A_loginpage import LoginPage
from Utilities.ReadProperties import ReadConfig
from Utilities.BaseHelpers import BaseHelper
from datetime import datetime
from py.xml import html
import os
import re


# --------------------------
# CLI Options
# --------------------------
def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chromium",
                     help="Browser: chromium/firefox/webkit")
    parser.addoption("--region", action="store", default="AP",
                     help="Region: AP/ME/US/EU/Test")
    parser.addoption("--headless", action="store_true",
                     help="Run in headless mode")


# --------------------------
# Playwright Instance
# --------------------------
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as pw:
        yield pw


# --------------------------
# Launch Fresh Browser per Test
# --------------------------
@pytest.fixture(scope="function")
def browser(playwright_instance, request) -> Browser:
    browser_name = request.config.getoption("--browser_name")
    headless = request.config.getoption("--headless")

    if browser_name.lower() == "chromium":
        browser = playwright_instance.chromium.launch(headless=headless)
    elif browser_name.lower() == "firefox":
        browser = playwright_instance.firefox.launch(headless=headless)
    elif browser_name.lower() == "webkit":
        browser = playwright_instance.webkit.launch(headless=headless)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    yield browser
    browser.close()


# --------------------------
# Fresh Page for Every Test
# --------------------------
@pytest.fixture(scope="function")
def page(browser) -> Page:
    context = browser.new_context(viewport={"width": 1470, "height": 720})
    page = context.new_page()
    yield page
    context.close()


# --------------------------
# Login Fixture (Optional)
# --------------------------
@pytest.fixture(scope="function")
def login(page, request) -> Page:
    region = request.config.getoption("--region")

    url = ReadConfig.getURL(region)
    client_id = ReadConfig.getClientID(region)
    username = ReadConfig.getUsername(region)
    password = ReadConfig.getPassword(region)

    print(f"\n➡️ Launching URL: {url} ({region})")
    page.goto(url)

    lp = LoginPage(page)
    lp.setClientid(client_id)
    lp.setUserName(username)
    lp.setPassword(password)
    lp.clickLogin()

    helper = BaseHelper(page)
    helper.verify_page_url("/dashboard", description="Dashboard")

    yield page


# ------------------------------
# Custom HTML Report Configuration
# ------------------------------

@pytest.mark.optionalhook
def pytest_html_report_title(report):
    report.title = "🚀 Cflow Playwright Automation Report"


@pytest.mark.optionalhook
def pytest_configure(config):
    """Disable built-in metadata to hide the environment table."""
    config._metadata = {}
    config.option.metadata = {}
    config._environment = False


@pytest.mark.optionalhook
def pytest_metadata(metadata):
    """Ensure no leftover metadata."""
    metadata.clear()


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    """Add clean custom summary line."""
    timestamp = datetime.now().strftime("%d-%b-%Y %H:%M:%S")

    # Custom info
    projectname = "Cflow Playwright Automation"
    modulename = "Admin Module - Add User"
    tester = "Dinesh Aravinth ⚡"
    browser = "Chromium"
    region = "TEST"

    style = (
        "background: #ffffff;"
        "padding: 12px 18px;"
        "font-family: Verdana, sans-serif;"
        "font-size: 16px;"
        "font-weight: 600;"
        "color: #000000;"
        "display: flex;"
        "align-items: center;"
        "white-space: nowrap;"
    )

    separator_style = "margin: 0 10px; font-weight: bold; color: #000000;"

    metadata_html = html.tr([
        html.td([
            html.span("📄 Project: ", style="font-weight:bold;"),
            html.span(projectname),

            html.span("🏆", style=separator_style),

            html.span("📁 Module: ", style="font-weight:bold;"),
            html.span(modulename),

            html.span(" | ", style=separator_style),

            html.span("👤 Tester: ", style="font-weight:bold;"),
            html.span(tester),

            html.span(" | ", style=separator_style),

            html.span("🌐 Browser: ", style="font-weight:bold;"),
            html.span(browser),

            html.span(" | ", style=separator_style),

            html.span("🌍 Region: ", style="font-weight:bold;"),
            html.span(region),

            html.span(" | ", style=separator_style),

            html.span("⏰ Execution: ", style="font-weight:bold;"),
            html.span(timestamp),
        ], style=style)
    ])

    prefix.append(metadata_html)


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    """Initialize session start time manually for pytest-html >= 8."""
    config = session.config
    terminal_reporter = config.pluginmanager.get_plugin("terminalreporter")
    if terminal_reporter and not hasattr(terminal_reporter, "_sessionstarttime"):
        from datetime import datetime
        terminal_reporter._sessionstarttime = datetime.now().timestamp()


# ------------------------------
# Remove Environment Section After Report Creation
# ------------------------------

def pytest_sessionfinish(session, exitstatus):
    """
    After report generation, strip out the entire Environment section.
    Works 100% for pytest-html 4.1.1.
    """
    report_path = getattr(session.config.option, "htmlpath", None)
    if report_path and os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Remove entire Environment <h2> section
        cleaned_html = re.sub(
            r"<h2>Environment<\/h2>.*?<table>.*?<\/table>", "", html_content, flags=re.S
        )

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(cleaned_html)


