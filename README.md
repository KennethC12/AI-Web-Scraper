# AI Web Scraper with LinkedIn Auto-Connector

This project is an AI-powered web scraper that automates web scraping tasks using Selenium and parses information using Llama 3.1. Additionally, it includes a LinkedIn auto-connector feature that allows users to automate LinkedIn connections based on custom prompts.

## Features

- **Automated Web Scraping**: Uses Selenium and BeautifulSoup4 to scrape data from websites.
- **AI Parsing**: Integrates with Llama 3.1 via Langchain to parse and analyze scraped information.
- **LinkedIn Auto-Connector**: Automates the process of sending connection requests on LinkedIn using custom user prompts.
- **Stealth Browsing**: Uses undetected-chromedriver to avoid detection during automated scraping and browsing.

## Technologies Used

- **Streamlit**: For building the front-end interface.
- **Langchain & langchain_ollama**: To interact with Llama 3.1 for parsing scraped content.
- **Selenium**: Automates browser interaction and scraping.
- **BeautifulSoup4, lxml, html5lib**: For parsing the HTML structure of websites.
- **python-dotenv**: For managing environment variables.
- **webdriver-manager & undetected-chromedriver**: Handles browser drivers and ensures the scraper is not easily detected.
  
## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/ai-web-scraper.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```


3. Run the project using:

    ```bash
    streamlit run app.py
    ```

## Usage

1. **Web Scraping**: After launching the application, input the website URL you wish to scrape, and the scraper will extract and display the relevant information.
   
2. **AI Parsing**: The scraped data will be parsed using Llama 3.1. You can interact with the output through the Langchain interface.
   
3. **LinkedIn Auto-Connector**: In the LinkedIn auto-connector tab, input your desired prompts for sending connection requests. The bot will automate sending connection invites based on your preferences.

## Notes

- This project is designed to avoid detection during scraping, but scraping some websites may still violate their terms of service. Use responsibly.
- The LinkedIn auto-connector should be used thoughtfully, following LinkedIn’s guidelines to avoid account issues.

## Contributions

Feel free to fork this repository and submit pull requests if you would like to contribute!

## License

This project is licensed under the MIT License.
