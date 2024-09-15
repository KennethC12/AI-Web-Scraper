import time
from threading import Thread
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Static Prompt Template
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Initialize the model once
model = OllamaLLM(model="llama3.1")


def process_chunk(chunk, parse_description):
    """
    Process a single chunk of DOM content with the model.
    """
    try:
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        return response
    except Exception as e:
        # Handle model or API errors
        return f"Error processing chunk: {str(e)}"


def parse_with_ollama(
    dom_chunks,
    parse_description,
    batch_size=5,
    throttle_time=2,
):
    """
    Process DOM content synchronously and return parsed results as a list.
    """
    total_chunks = len(dom_chunks)
    parsed_results = []

    # Process in batches
    for i in range(0, total_chunks, batch_size):
        batch = dom_chunks[i : i + batch_size]

        for j, chunk in enumerate(batch):
            response = process_chunk(chunk, parse_description)
            parsed_results.append(response)

            # Print progress
            current_chunk_number = i + j + 1
            progress_percentage = (current_chunk_number / total_chunks) * 100
            print(
                f"Processed {current_chunk_number}/{total_chunks} chunks ({progress_percentage:.2f}% complete)"
            )

        # Throttle requests
        if i + batch_size < total_chunks:
            time.sleep(throttle_time)

    return parsed_results


def run_parsing_in_thread(
    dom_chunks,
    parse_description,
    batch_size=5,
    throttle_time=2,
    output_file="parsed_results.txt",
):
    """
    Runs the parse_with_ollama function in a separate thread to prevent blocking the main thread.
    """
    parsing_thread = Thread(
        target=parse_with_ollama,
        args=(dom_chunks, parse_description, batch_size, throttle_time, output_file),
    )
    parsing_thread.start()
    print("Parsing has started in a separate thread.")
