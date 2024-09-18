import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def connect(
    website,
    login_url=None,
    username=None,
    password=None,
    num_pages=1,
    note_text="",
):
    print("Connecting to LinkedIn without Proxy...")

    # Initialize the undetected-chromedriver without a proxy
    driver = uc.Chrome(version_main=128)

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
            print("Login successful")

        # Navigate to the actual target page after logging in
        driver.get(website)
        print(f"Navigated to target page: {website}")

        # Loop through the specified number of pages
        for page in range(num_pages):
            print(f"Processing page {page + 1} of {num_pages}")

            connect_buttons = []
            try:
                # Try to find the "Connect" buttons within 10 seconds
                print("Looking for all 'Connect' buttons...")
                connect_buttons = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//button[contains(@aria-label, 'to connect')]")
                    )
                )
            except TimeoutException:
                print(
                    f"No 'Connect' buttons found on page {page + 1}. Attempting to scroll down..."
                )

                # Scroll down once if no "Connect" buttons are found
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)  # Wait for the page to load more content after scrolling

                # Try to find the "Connect" buttons again after scrolling
                try:
                    connect_buttons = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, "//button[contains(@aria-label, 'to connect')]")
                        )
                    )
                except TimeoutException:
                    print(
                        f"No 'Connect' buttons found after scrolling on page {page + 1}. Moving to next page..."
                    )

            # If we found "Connect" buttons after scrolling, process them
            if connect_buttons:
                print(
                    f"Found {len(connect_buttons)} 'Connect' buttons on page {page + 1}"
                )

                # Iterate through each connect button and handle Premium prompt if needed
                for connect_button in connect_buttons:
                    try:
                        connect_button.click()  # Step 1: Click "Connect"
                        print("Connect button clicked successfully.")

                        time.sleep(2)

                        # Step 2: Click "Add a note" button
                        print("Looking for the 'Add a note' button...")
                        add_note_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable(
                                (
                                    By.XPATH,
                                    "//button[contains(@aria-label, 'Add a note')]",
                                )
                            )
                        )
                        add_note_button.click()
                        print("Add a note button clicked successfully.")

                        time.sleep(2)  # Pause before adding the note

                        # Step 3: Wait for the note text area and add the note
                        note_textarea = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located(
                                (
                                    By.XPATH,
                                    "//textarea[contains(@id, 'custom-message')]",
                                )
                            )
                        )
                        note_textarea.send_keys(note_text)
                        print(f"Note added: {note_text}")

                        time.sleep(1)

                        # Step 4: Submit the connection request
                        send_invitation_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable(
                                (
                                    By.XPATH,
                                    "//button[contains(@aria-label, 'Send invitation')]",
                                )
                            )
                        )
                        send_invitation_button.click()
                        print("Invitation with note sent successfully.")

                    except TimeoutException:
                        # Step 5: Handle LinkedIn Premium prompt if it appears
                        print("Premium prompt detected, dismissing it...")
                        premium_prompt = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//button[@aria-label='Dismiss']")
                            )
                        )
                        premium_prompt.click()
                        print("Premium prompt dismissed.")

                        time.sleep(2)  # Wait for the modal to close

                        # Step 6: Click "Connect" again after dismissing the Premium prompt
                        print(
                            "Clicking 'Connect' button again after dismissing Premium prompt."
                        )
                        connect_button.click()

                        time.sleep(2)

                        # Step 7: Click "Send without a note"
                        try:
                            send_without_note_button = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable(
                                    (
                                        By.XPATH,
                                        "//button[@aria-label='Send without a note']",
                                    )
                                )
                            )
                            send_without_note_button.click()
                            print(
                                "Sent connection without a note after re-clicking Connect."
                            )
                        except TimeoutException:
                            print(
                                "Could not find the 'Send without a note' button after re-clicking Connect."
                            )

                    except Exception as e:
                        print(f"An error occurred while trying to connect: {str(e)}")
                        continue  # Continue with the next "Connect" button

            # After processing the page, move to the next page
            print("Looking for the 'Next' button...")
            try:
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

                time.sleep(5)  # Wait for the next page to load
            except TimeoutException:
                print("No more 'Next' button found. Reached the final page.")
                break
            except Exception as e:
                print(
                    f"An error occurred while trying to click the 'Next' button: {str(e)}"
                )
                break

    except TimeoutException as e:
        print(f"An error occurred during login: {str(e)}")

    return driver  # Return the driver to allow further actions
