import os
from datetime import datetime
from playwright.sync_api import Page, TimeoutError


class BaseHelper:
    def __init__(self, page: Page):
        self.page = page
        self.screenshot_dir = r"D:\CFLOW PLAYWRIGHT\Screenshots"

    # ---------------------------------------------------------------
    # Utility: Screenshot
    # ---------------------------------------------------------------
    def take_screenshot(self, prefix="Error"):
        os.makedirs(self.screenshot_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(self.screenshot_dir, f"{prefix}_{timestamp}.png")
        self.page.screenshot(path=screenshot_path)
        print(f"📸 Screenshot saved at: {screenshot_path}")
        return screenshot_path

    # ---------------------------------------------------------------
    # Common Actions
    # ---------------------------------------------------------------
    def click(self, locator, description: str = "element", timeout: int = 5000):
        """Click an element and stop test on failure."""
        try:
            element = self.page.locator(locator) if isinstance(locator, str) else locator
            element.wait_for(state="visible", timeout=timeout)
            element.scroll_into_view_if_needed()
            element.click(timeout=timeout)
            print(f"✅ Clicked: {description}")

        except Exception as e:
            self.take_screenshot(f"ClickFailed_{description.replace(' ', '_')}")
            error_msg = f"❌ Test failed — Unable to click {description}: {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    def enter_text(self, locator, text: str, description: str = "textbox", timeout: int = 5000):
        """Enter text into a field and stop test on failure."""
        try:
            element = self.page.locator(locator) if isinstance(locator, str) else locator
            element.wait_for(state="visible", timeout=timeout)
            element.scroll_into_view_if_needed()
            element.fill("")  # Clear any existing text
            element.fill(text)
            print(f"✅ Entered '{text}' into {description}")

        except Exception as e:
            self.take_screenshot(f"EnterTextFailed_{description.replace(' ', '_')}")
            error_msg = f"❌ Test failed — Unable to enter text in {description}: {e}"
            print(error_msg)
            raise AssertionError(error_msg)


    def scroll_to_label(self, locator, friendly_name: str = None, timeout: int = 5000):
        """
        Scroll to any element and confirm it's visible on the page.

        Args:
            locator (str | Locator): XPath/CSS selector or Playwright locator.
            friendly_name (str): Optional readable name for better console logs.
            timeout (int): How long to wait for element visibility in ms.

        Returns:
            Locator: The visible locator object for further actions (click, type, etc.)
        """
        try:
            # Allow both string and Locator objects
            element = self.page.locator(locator) if isinstance(locator, str) else locator

            # Wait for it to appear and be visible
            element.wait_for(state="visible", timeout=timeout)

            # Scroll into view if needed
            element.scroll_into_view_if_needed()

            # Print readable element info
            label_text = friendly_name or element.inner_text(timeout=1000) or "Unnamed Element"
            print(f"✅ Element visible — {label_text.strip()}")

            return element

        except Exception as e:
            self.take_screenshot(f"ElementNotVisible_{friendly_name or 'Unknown'}")
            error_msg = f"❌ Test failed — Element not visible or scroll failed: {friendly_name or locator}: {e}"
            print(error_msg)
            raise AssertionError(error_msg)

    # ---------------------------------------------------------------
    # Page Verification
    # ---------------------------------------------------------------
    def verify_page_url(self, expected_url_fragment: str, description: str = "page", timeout: int = 10000):
        """Verify the page URL contains the expected fragment."""
        try:
            print(f"🌍 Verifying {description} URL ...")
            self.page.wait_for_url(f"**{expected_url_fragment}**", timeout=timeout)
            actual_url = self.page.url

            if expected_url_fragment in actual_url:
                print(f"🏆 {description} URL verification passed! ✅")
                print(f"Actual URL: '{actual_url}'")
            else:
                raise AssertionError(
                    f"❌ {description} URL verification failed.\n"
                    f"Expected fragment: '{expected_url_fragment}'\n"
                    f"Actual URL: '{actual_url}'"
                )

        except Exception as e:
            self.take_screenshot(f"URL_Verification_Failed_{description.replace(' ', '_')}")
            # Include expected/actual URL in the exception if possible
            actual_url = getattr(self.page, "url", "N/A")  # fallback if page.url not available
            error_msg = (
                f"❌ Test failed — {description} URL verification failed: {e}\n"
                f"Expected fragment (url to be): '{expected_url_fragment}'\n"
                f"Actual URL: '{actual_url}'"
            )
            print(error_msg)
            raise AssertionError(error_msg)





