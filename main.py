import streamlit as st
import time
from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content,
)
from linkedinscrape import (
    linkedinscrape_website,
    extract_body_content,
    clean_body_content,
)
from parse import (
    parse_with_ollama,
    process_chunk,
)  # Ensure these are correctly imported
from linkedinconnect import linkedin_scrapepages

# Sidebar Navigation for Multi-Page Experience
page = st.sidebar.selectbox(
    "Navigate", ["Home", "Scrape Website", "Login and Scrape", "Linkedin Connect"]
)

# Home Page
if page == "Home":
    st.title("Welcome to the Web Scraper")
    st.write("Use the sidebar to navigate between pages.")

# Scrape Website Page (without login)
elif page == "Scrape Website":
    st.title("Web Scraper")

    # URL input field
    url = st.text_input("Enter URL")

    # Button to start scraping the site
    if st.button("Scrape Site"):
        if not url:
            st.error("Please enter a valid URL.")
        else:
            st.write("Scraping the website...")
            try:
                with st.spinner("Scraping the website..."):
                    result = scrape_website(website=url)
            except Exception as e:
                st.error(f"An error occurred while scraping: {str(e)}")
                result = None

            # If scraping succeeds, clean and display content
            if result:
                body_content = extract_body_content(result)  # Extract body from HTML
                cleaned_content = clean_body_content(body_content)  # Clean content
                st.session_state.dom_content = cleaned_content  # Save in session state

                # Display the DOM content in an expandable text area
                with st.expander("View DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)
            else:
                st.error("Failed to scrape the website.")

    # Parsing section after scraping is complete
    if "dom_content" in st.session_state:
        parse_description = st.text_area(
            "Describe what you want to parse?",
            value="",
            placeholder="Enter your parsing instructions here...",
        )

        if st.button("Parse Content"):
            if parse_description:
                st.write("Parsing the content...")
                dom_chunks = split_dom_content(
                    st.session_state.dom_content
                )  # Split DOM into chunks

                # Initialize progress indicators
                progress_bar = st.progress(0)
                progress_text = st.empty()

                try:
                    total_chunks = len(dom_chunks)
                    parsed_results = []

                    for i, chunk in enumerate(dom_chunks):
                        response = process_chunk(chunk, parse_description)
                        parsed_results.append(response)

                        # Update progress
                        progress_percentage = (i + 1) / total_chunks
                        progress_bar.progress(progress_percentage)
                        progress_text.text(f"Processed {i + 1}/{total_chunks} chunks")

                    result = "\n".join(parsed_results)
                    st.write("Parsing complete.")

                    # Display the parsed content
                    parsed_result = parse_with_ollama(dom_chunks, parse_description)
                    st.write(parsed_result)
                except Exception as e:
                    st.error(f"An error occurred while parsing: {str(e)}")
            else:
                st.error("Please provide a description for what you want to parse.")

# Login and Scrape Page (input both login details and URL, then scrape)
elif page == "Login and Scrape":
    st.title("Login and Scrape")

    # URL input field
    url = st.text_input("Enter URL")

    # Input login credentials
    login_url = st.text_input("Login URL (if different from main URL)", value=url)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # Button to start login and scraping
    if st.button("Login and Scrape"):
        if not url or not login_url or not email or not password:
            st.error("URL, login URL, email, and password are required.")
        else:
            st.write("Logging into LinkedIn and scraping the content...")
            try:
                with st.spinner("Logging in and scraping the website..."):
                    # Use the linkedin_scrape function from linkedinscrape.py
                    result = linkedinscrape_website(
                        website=url,  # URL to scrape after login
                        login_url=login_url,  # Login URL
                        username=email,  # Email for login
                        password=password,  # Password for login
                    )
            except Exception as e:
                st.error(f"An error occurred during login: {str(e)}")
                result = None

            # If scraping succeeds, clean and display content
            if result:
                body_content = extract_body_content(result)  # Extract body from HTML
                cleaned_content = clean_body_content(body_content)  # Clean content
                st.session_state.dom_content = cleaned_content  # Save in session state

                # Display the DOM content in an expandable text area
                with st.expander("View DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)
            else:
                st.error("Failed to scrape the website.")

    # Parsing section after scraping is complete
    if "dom_content" in st.session_state:
        parse_description = st.text_area(
            "Describe what you want to parse?",
            value="",
            placeholder="Enter your parsing instructions here...",
        )

        # Inside the parsing section
        if st.button("Parse Content"):
            if parse_description:
                st.write("Parsing the content...")

                # Split DOM into chunks
                dom_chunks = split_dom_content(st.session_state.dom_content)

                # Initialize progress indicators
                progress_bar = st.progress(0)
                progress_text = st.empty()

                try:
                    total_chunks = len(dom_chunks)
                    parsed_results = []

                    for i, chunk in enumerate(dom_chunks):
                        response = process_chunk(chunk, parse_description)
                        parsed_results.append(response)

                        # Update progress
                        progress_percentage = (i + 1) / total_chunks
                        progress_bar.progress(progress_percentage)
                        progress_text.text(f"Processed {i + 1}/{total_chunks} chunks")

                    st.write("Parsing complete.")

                    # Display the parsed content
                    parsed_result = parse_with_ollama(dom_chunks, parse_description)
                    st.write(parsed_result)
                except Exception as e:
                    st.error(f"An error occurred while parsing: {str(e)}")
            else:
                st.error("Please provide a description for what you want to parse.")


elif page == "Linkedin Connect":
    st.title("Linkedin")

    # URL input field
    url = st.text_input("Enter URL")

    # Input login credentials
    login_url = st.text_input("Login URL (if different from main URL)", value=url)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    num_pages = st.number_input(
        "Number of pages to scrape", min_value=1, value=1, step=1
    )

    # Button to start login and scraping
    if st.button("Login and Scrape"):
        if not url or not login_url or not email or not password:
            st.error("URL, login URL, email, and password are required.")
        else:
            st.write("Logging into LinkedIn and scraping the content...")
            try:
                with st.spinner("Logging in and scraping the website..."):
                    # Use the linkedin_scrape function from linkedinscrape.py
                    result = linkedin_scrapepages(
                        website=url,  # URL to scrape after login
                        login_url=login_url,  # Login URL
                        username=email,  # Email for login
                        password=password,  # Password for login
                        num_pages=num_pages,
                    )
            except Exception as e:
                st.error(f"An error occurred during login: {str(e)}")
                result = None

            # If scraping succeeds, clean and display content
            if result:
                all_cleaned_content = []
                for html_content in result:
                    body_content = extract_body_content(html_content)
                    cleaned_content = clean_body_content(body_content)
                    all_cleaned_content.append(cleaned_content)

                combined_cleaned_content = "\n".join(all_cleaned_content)

                st.session_state.dom_content = combined_cleaned_content
                # Display the DOM content in an expandable text area
                with st.expander("View DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)
            else:
                st.error("Failed to scrape the website.")

    # Parsing section after scraping is complete
    if "dom_content" in st.session_state:
        parse_description = st.text_area(
            "Describe what you want to parse?",
            value="",
            placeholder="Enter your parsing instructions here...",
        )

        # Inside the parsing section
        if st.button("Parse Content"):
            if parse_description:
                st.write("Parsing the content...")

                # Split DOM into chunks
                dom_chunks = split_dom_content(st.session_state.dom_content)

                # Initialize progress indicators
                progress_bar = st.progress(0)
                progress_text = st.empty()

                try:
                    total_chunks = len(dom_chunks)
                    parsed_results = []

                    for i, chunk in enumerate(dom_chunks):
                        response = process_chunk(chunk, parse_description)
                        parsed_results.append(response)

                        # Update progress
                        progress_percentage = (i + 1) / total_chunks
                        progress_bar.progress(progress_percentage)
                        progress_text.text(f"Processed {i + 1}/{total_chunks} chunks")

                    st.write("Parsing complete.")

                    # Display the parsed content
                    parsed_result = parse_with_ollama(dom_chunks, parse_description)
                    st.write(parsed_result)
                except Exception as e:
                    st.error(f"An error occurred while parsing: {str(e)}")
            else:
                st.error("Please provide a description for what you want to parse.")
