import os
from bs4 import BeautifulSoup
import html2text
import json
from typing import List
import logging

# Constants for file paths
PAGES_FOLDER_PATH = "../../data/Bill_FAQs/pages"
QNA_PATH = '../../data/Bill_FAQs'
PARSED_DATA_PATH = '../../data/Bill_FAQs/parsed'
ALL_QUESTIONS_MD_FILE = os.path.join(QNA_PATH, 'all.md')

LOGGING_SCRAPING_PATH = '../../logs/scraping_logs.txt'

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOGGING_SCRAPING_PATH), logging.StreamHandler()],
)


def get_files(folder_path: str) -> List[str]:
    """
    Retrieve a list of file paths from the specified directory.

    Args:
        folder_path (str): The directory path from which to retrieve file paths.

    Returns:
        List[str]: A list of absolute file paths.
    """
    files = []

    # Iterate over the files in the directory and append their absolute paths to the list
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            files.append(file_path)

    return files


def process_page_source(page_path: str) -> dict:
    """
    Process an HTML page to extract the question (title) and the answer,
    converting the answer to markdown format.

    Args:
        page_path (str): The file path of the HTML page.

    Returns:
        dict: A dictionary containing the page URL, title, title formatted for file naming,
              and the answer in markdown format.
    """
    with open(page_path, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Extract the title (question) and the answer from the HTML content
    title = soup.find('h2', class_="article-head").get_text(strip=True)
    answer = soup.find('div', class_="uiOutputRichText")

    # Convert the answer from HTML to Markdown format
    h = html2text.HTML2Text()
    markdown_text = h.handle(str(answer))

    # Generate a title suitable for use as a filename
    title_file = title.lower().replace(' ', '_').replace("/", "")

    return {
        "page_url": page_path,
        "title": title,
        "title_file": title_file,
        # "answer_html": answer.prettify(),  # Uncomment to include HTML format if needed
        "answer_markdown": markdown_text
    }


def main():
    # Get the list of HTML files to process
    files = get_files(PAGES_FOLDER_PATH)

    # Extract information from each HTML file
    processed_pages = [process_page_source(file) for file in files]
    logging.info(f"Number of processed pages: {len(processed_pages)}")

    # Save all parsed Q&A data to a JSONL file
    qnas_filename = os.path.join(QNA_PATH, 'qnas.jsonl')
    with open(qnas_filename, 'w') as f:
        json.dump(processed_pages, f)
    logging.info(f"Processed pages saved to: {qnas_filename}")

    # Save each Q&A as a separate markdown (.md) file
    logging.info("Saving individual markdown files for each question...")
    for n, page in enumerate(processed_pages):
        filename = os.path.join(PARSED_DATA_PATH, page['title_file'] + '.md')
        logging.info(f"Saving file {n}: {filename}")

        content = page["title"] + '\n' + page["answer_markdown"] + '\n\n'

        with open(filename, 'w') as f:
            f.write(content)
    logging.info("All individual markdown files saved.")

    # Save all Q&As to a single markdown file
    logging.info("Saving all questions to a single markdown file...")
    text = ''
    for page in processed_pages:
        document_text = page["title"] + ' \n ' + page["answer_markdown"] + ' \n\n '
        text += document_text

    with open(ALL_QUESTIONS_MD_FILE, 'w') as f:
        f.write(text)
    logging.info(f"All questions saved to: {ALL_QUESTIONS_MD_FILE}")


if __name__ == "__main__":
    main()
