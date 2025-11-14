import pytest
from playwright.sync_api import sync_playwright, Browser, Page
from PageObjects.Login_Page.A_loginpage import LoginPage
from Utilities.ReadProperties import ReadConfig
from Utilities.BaseHelpers import BaseHelper
from datetime import datetime
from py.xml import html
import os
import re

# ---------- Global setup (manual control) ----------
# Start Playwright once globally
playwright = sync_playwright().start()
browser = None
context = None
page = None


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name",
        action="store",
        default="chromium",
        help="Browser to run tests on: chromium/firefox/webkit"
    )
    parser.addoption(
        "--region",
        action="store",
        default="AP",
        help="Region to run tests on: AP/ME/US/EU/Test"
    )
    parser.addoption(
        "--keep-open",
        action="store_true",
        help="Keep browser open after tests"
    )


@pytest.fixture(scope="session")
def browser_page(request):
    """Launch Playwright browser and keep it open after tests."""
    global browser, context, page

    browser_name = request.config.getoption("--browser_name")
    region = request.config.getoption("--region")
    keep_open = request.config.getoption("--keep-open")

    print(f"\n🌍  Launching {browser_name} for region {region}")

    if browser_name.lower() == "chromium":
        browser = playwright.chromium.launch(
            headless=False,
            args=["--start-maximized", "--window-position=0,0", "--window-size=1536,864"]
        )
    elif browser_name.lower() == "firefox":
        browser = playwright.firefox.launch(headless=False)
    elif browser_name.lower() == "webkit":
        browser = playwright.webkit.launch(headless=False)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    context = browser.new_context(viewport={"width": 1450, "height": 720})
    page = context.new_page()

    yield page

    # ✅ Keep browser open for debugging
    if keep_open:
        print("\n🧭 Browser will remain open for manual inspection...")
        print("❗ Close it manually when done.")
        input("Press ENTER here in terminal to close browser...")

    # Only close if user didn’t request to keep open
    else:
        print("🧹 Closing browser automatically...")
        browser.close()
        playwright.stop()


@pytest.fixture(scope="session")
def login(browser_page, request):
    """Login once per session and return logged-in Playwright page."""
    page = browser_page
    region = request.config.getoption("--region")

    try:
        url = ReadConfig.getURL(region)
        client_id = ReadConfig.getClientID(region)
        username = ReadConfig.getUsername(region)
        password = ReadConfig.getPassword(region)

        print(f"➡️  Navigating to URL: {url} for region: {region}")
        page.goto(url)

        # Perform login
        lp = LoginPage(page)
        lp.setClientid(client_id)
        lp.setUserName(username)
        lp.setPassword(password)
        lp.clickLogin()

        # Verify post-login page URL
        helper = BaseHelper(page)
        expected_url_fragment = "/dashboard"  # Replace with your actual post-login URL fragment
        helper.verify_page_url(expected_url_fragment,description="Dashboard")

    except Exception as e:
        print(f"❌ Login failed: {e}")
        raise e  # Fail the test immediately if login or URL verification fails

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


@pytest.fixture(scope="session")
def playwright_instance():
    """
    Start a single Playwright instance for the entire test session.
    """
    with sync_playwright() as pw:
        yield pw
    # Playwright stops automatically when exiting the context


@pytest.fixture(scope="session")
def browser(playwright_instance) -> Browser:
    """
    Launch a persistent browser for the test session.
    """
    browser = playwright_instance.chromium.launch(headless=False)
    yield browser
    browser.close()


@pytest.fixture
def page(browser) -> Page:
    """
    Create a fresh page for each test. Uses the session-scoped browser.
    """
    context = browser.new_context(viewport={"width": 1470, "height": 720})
    page = context.new_page()
    yield page
    context.close()