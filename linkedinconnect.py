import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import time


def linkedin_scrapepages(
    website, login_url=None, username=None, password=None, num_pages=1, scroll_times=1
):
    print("Connecting to Scraping Browser without Proxy...")

    # Initialize the undetected-chromedriver without a proxy
    driver = uc.Chrome()

    all_page_contents = []  # To store the HTML content of each page

    try:
        # If login is required, log in first
        if login_url and username and password:
            driver.get(login_url)
            print(f"Opened login page: {login_url}")

            time.sleep(2)

            # Wait for the username field to become visible
            username_field = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="username"]'))
            )
            username_field.send_keys(username)

            time.sleep(3)

            # Wait for the password field to become visible
            password_field = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="password"]'))
            )
            password_field.send_keys(password)

            time.sleep(2)

            # Wait for the submit button to become clickable and click it
            submit_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[@aria-label="Sign in" and @type="submit"]')
                )
            )
            submit_button.click()

            time.sleep(5)  # Wait for login to complete and page to load

        # Navigate to the actual target page after logging in
        driver.get(website)
        print(f"Navigated to target page: {website}")

        for page in range(num_pages):
            # Perform scrolling for dynamic content loading
            for scroll in range(scroll_times):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Wait for the page to load more content
                print(f"Scrolled {scroll + 1} times on page {page + 1}.")

            # Scrape the current page content
            html = driver.page_source
            all_page_contents.append(html)

            # Extract body content from the current page
            body_content = extract_body_content(html)
            cleaned_content = clean_body_content(body_content)
            print(f"Scraped page {page + 1} content of length {len(cleaned_content)}")

            try:
                # Try to find and click the "Next" button using the provided XPath
                print("Looking for the 'Next' button...")
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[@aria-label='Next' and contains(@class, 'artdeco-pagination__button--next')]",
                        )
                    )
                )
                print("Next button found. Clicking...")
                next_button.click()

                time.sleep(3)  # Wait for the next page to load
            except TimeoutException:
                # If no "Next" button is found, break the loop
                print("No more 'Next' button found. Reached the final page.")
                break
            except Exception as e:
                print(
                    f"An error occurred while trying to click the 'Next' button: {str(e)}"
                )
                break

        return all_page_contents  # Return the HTML content of all pages

    except TimeoutException as e:
        print(f"Timeout while waiting for element: {str(e)}")
        driver.save_screenshot("error_screenshot.png")
        raise Exception(f"TimeoutException: {str(e)}")

    except NoSuchElementException as e:
        print(f"Element not found: {str(e)}")
        driver.save_screenshot("error_screenshot.png")
        raise Exception(f"NoSuchElementException: {str(e)}")

    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        driver.save_screenshot("error_screenshot.png")
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


def connect(): ...
