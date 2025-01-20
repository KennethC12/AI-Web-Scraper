from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")


# Function to scrape a website
def scrape_website(website):
    print("Connecting to Scraping Browser...")
    sbr_connection = ChromiumRemoteConnection(
        SBR_WEBDRIVER, "goog", "chrome"
    )  # This is the connection to the browser
    with Remote(
        sbr_connection, options=ChromeOptions()
    ) as driver:  # This is the driver
        driver.get(website)  # Navigating to the website
        print("Waiting captcha to solve...")
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",  # Captcha solver
                "params": {"detectTimeout": 10000},  # Timeout
            },
        )
        print("Captcha solve status:", solve_res["value"]["status"])
        print("Navigated! Scraping page content...")
        html = driver.page_source  # Scraping the page content
        return html


# Function to extract the body content
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")  # Parsing the HTML
    body_content = soup.body
    if body_content:  # If the body content exists
        return str(body_content)
    return ""


# Function to clean the body content
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):  # Removing scripts and styles
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(  # Removing empty lines
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


# Function to split the DOM content
def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
