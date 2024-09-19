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
    add_note=False,  # Checkbox control to decide if note should be added
    note_text=None,  # Changed default to None to handle no note scenario
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

                # Iterate through each connect button and handle the connection
                for connect_button in connect_buttons:
                    try:
                        connect_button.click()  # Step 1: Click "Connect"
                        print("Connect button clicked successfully.")

                        time.sleep(2)

                        # Handle sending the connection based on whether to add a note or not
                        if add_note and note_text:  # Send connection with a note
                            print("Adding a note to the connection request...")

                            # Step 2: Click "Add a note" button
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

                            # Step 4: Submit the connection request with the note
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

                        else:  # Send connection without a note
                            print("Sending connection without a note.")
                            send_without_note_button = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable(
                                    (
                                        By.XPATH,
                                        "//button[contains(@aria-label, 'Send without a note') and contains(@class, 'artdeco-button--primary')]",
                                    )
                                )
                            )
                            send_without_note_button.click()
                            print("Invitation without note sent successfully.")

                    except TimeoutException:
                        print("Premium prompt detected or other issue occurred.")
                        continue  # Skip to the next connection button

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

    finally:
        # Ensure the driver is closed after everything is done
        print("Closing the browser...")
        driver.quit()

    return driver  # Return the driver to allow further actions
