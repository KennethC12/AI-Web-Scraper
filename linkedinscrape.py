import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import time


def linkedinscrape_website(website, login_url=None, username=None, password=None):

    print("Connecting to Scraping Browser without Proxy...")

    # Initialize the undetected-chromedriver without a proxy
    driver = uc.Chrome(version_main=128)

    try:
        # If login is required, go to the login page first
        if login_url and username and password:
            driver.get(login_url)
            print(f"Opened login page: {login_url}")

            time.sleep(2)

            # Wait for the username field to become visible
            print("Waiting for username field...")
            username_field = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))
            )
            print("Username field found. Entering username...")
            username_field.send_keys(username)

            time.sleep(3)

            # Wait for the password field to become visible
            print("Waiting for password field...")
            password_field = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="password"]'))
            )
            print("Password field found. Entering password...")
            password_field.send_keys(password)

            time.sleep(2)

            # Wait for the submit button to become clickable
            print("Waiting for submit button...")
            submit_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[@aria-label="Sign in" and @type="submit"]')
                )
            )
            print("Submit button found. Clicking...")
            submit_button.click()

            print("Waiting for captcha to solve (if applicable)...")

            # Optional Captcha solve logic (usually handled manually)
            try:
                solve_res = driver.execute(
                    "executeCdpCommand",
                    {
                        "cmd": "Captcha.waitForSolve",
                        "params": {"detectTimeout": 10000},
                    },
                )
                print("Captcha solve status:", solve_res["value"]["status"])
            except Exception as e:
                print("No captcha detected or solving failed:", str(e))

        # Navigate to the actual website after logging in
        driver.get(website)
        print(f"Navigated to target page: {website}")

        # Scrape the page content
        html = driver.page_source
        return html

    except TimeoutException as e:
        print(f"Timeout while waiting for element: {str(e)}")
        driver.save_screenshot("error_screenshot.png")  # Capture screenshot on timeout
        raise Exception(f"TimeoutException: {str(e)}")

    except NoSuchElementException as e:
        print(f"Element not found: {str(e)}")
        driver.save_screenshot(
            "error_screenshot.png"
        )  # Capture screenshot on element not found
        raise Exception(f"NoSuchElementException: {str(e)}")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        driver.save_screenshot(
            "error_screenshot.png"
        )  # Capture screenshot on unexpected errors
        raise Exception(f"Exception: {str(e)}")

    finally:
        driver.quit()  # Close the browser


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
