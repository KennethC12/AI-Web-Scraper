import time
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


def parse_with_ollama(
    dom_chunks, parse_description, batch_size=5, throttle_time=2, progress_callback=None
):
    """
    Process DOM content synchronously in batches with ChatPromptTemplate.
    Returns parsed results as a list.
    """
    # Initialize ChatPromptTemplate and chain
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    total_chunks = len(dom_chunks)
    parsed_results = []

    # Process in batches
    for i in range(0, total_chunks, batch_size):
        batch = dom_chunks[i : i + batch_size]

        for j, chunk in enumerate(batch, start=1):
            try:
                # Process the chunk using the chain
                response = chain.invoke(
                    {"dom_content": chunk, "parse_description": parse_description}
                )

                # Append the response or handle empty responses
                parsed_results.append(
                    response if response else "No result for this chunk."
                )

            except Exception as e:
                # Handle errors and append the error message to results
                parsed_results.append(f"Error processing chunk: {str(e)}")

            # Update progress after processing each chunk
            if progress_callback:
                # Calculate progress based on the number of chunks processed
                progress_percentage = (i + j) / total_chunks
                progress_callback(progress_percentage)

        # Throttle requests to avoid overloading resources
        if i + batch_size < total_chunks:
            time.sleep(throttle_time)

    # Return the combined parsed results as a string
    return "\n".join(parsed_results) if parsed_results else "No results to display."
