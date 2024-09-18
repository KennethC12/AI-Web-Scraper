import streamlit as st
import time
from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content,
)
from linkedinscrape import linkedinscrape_website
from parse import parse_with_ollama  # Ensure these are correctly imported
from linkedinconnect import connect

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

                # Split the DOM content into smaller chunks
                dom_chunks = split_dom_content(st.session_state.dom_content)

                # Initialize progress indicators
                progress_bar = st.progress(0)
                progress_text = st.empty()

                # Progress callback for updating the progress bar
                def update_progress_bar(progress_percentage):
                    progress_bar.progress(progress_percentage)

                try:
                    # Call parse_with_ollama and pass the progress callback
                    parsed_results = parse_with_ollama(
                        dom_chunks,
                        parse_description,
                        batch_size=5,
                        throttle_time=2,
                        progress_callback=update_progress_bar,
                    )

                    # Display parsed content once all chunks are processed
                    if parsed_results:
                        st.write("Parsing complete.")
                        st.write(parsed_results)
                    else:
                        st.error("Parsing returned no results.")

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

                # Split the DOM content into smaller chunks
                dom_chunks = split_dom_content(st.session_state.dom_content)

                # Initialize progress indicators
                progress_bar = st.progress(0)

                # Progress callback for updating the progress bar
                def update_progress_bar(progress_percentage):
                    # Ensure the value stays between 0.0 and 1.0
                    progress_percentage = min(max(progress_percentage, 0.0), 1.0)
                    progress_bar.progress(progress_percentage)

                try:
                    # Call parse_with_ollama and pass the progress callback
                    parsed_results = parse_with_ollama(
                        dom_chunks,
                        parse_description,
                        batch_size=5,
                        throttle_time=2,
                        progress_callback=update_progress_bar,
                    )

                    # Check if valid parsed results exist
                    if isinstance(parsed_results, list) and parsed_results:
                        result = "\n".join(parsed_results)
                    elif isinstance(parsed_results, str) and parsed_results.strip():
                        result = parsed_results
                    else:
                        st.error("Parsing resulted in no data or empty content.")

                    # Parsing is complete only when we have valid results
                    st.write("Parsing complete.")

                    # Display the final parsed content
                    st.write(result)

                except Exception as e:
                    st.error(f"An error occurred while parsing: {str(e)}")
            else:
                st.error("Please provide a description for what you want to parse.")


# Page for LinkedIn Connect
elif page == "Linkedin Connect":
    st.title("LinkedIn Connect")

    # URL input field
    url = st.text_input("Enter URL")

    # Input login credentials
    login_url = st.text_input("Login URL (if different from main URL)", value=url)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    num_pages = st.number_input(
        "Number of pages to process", min_value=1, value=1, step=1
    )

    # Input for note text
    note_text = st.text_area(
        "Enter the note to add to the connection request",
        placeholder="Write a note to include with your connection request...",
        value="",
    )

    # Button to start login and connecting
    if st.button("Login and Connect"):
        if not url or not login_url or not email or not password:
            st.error("URL, login URL, email, and password are required.")
        else:
            st.write("Logging into LinkedIn and sending connection requests...")
            try:
                with st.spinner("Logging in and sending connection requests..."):
                    # Use the connect function to send the connection requests
                    result = connect(
                        website=url,  # URL to connect after login
                        login_url=login_url,  # Login URL
                        username=email,  # Email for login
                        password=password,  # Password for login
                        num_pages=num_pages,  # Number of pages to process
                        note_text=note_text,  # Note text for the connection request
                    )
                    st.success("Connection requests sent successfully!")
            except Exception as e:
                st.error(f"An error occurred during login or connecting: {str(e)}")
