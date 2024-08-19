import os
from bs4 import BeautifulSoup
import html2text
import json

folder_path = "../../data/Bill_FAQs/pages"


def get_files(folder_path):
    files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            files.append(file_path)

    return files


def process_page_source(page_path):
    with open(page_path, 'r') as f:
        soup = BeautifulSoup(f.read())

    title = soup.find('h2', class_="article-head").get_text(strip=True)
    answer = soup.find('div', class_="uiOutputRichText")

    h = html2text.HTML2Text()
    markdown_text = h.handle(str(answer))

    title_file = title.lower().replace(' ', '_').replace("/", "")

    return {
        "page_url": page_path,
        "title": title,
        "title_file": title_file,
        "answer_html": answer.prettify(),
        "answer_markdown": markdown_text
    }


files = get_files(folder_path)
processed_pages = [process_page_source(file) for file in files]

QNA_PATH = '../../data/Bill_FAQs'
qnas_filename = os.path.join(QNA_PATH, 'qnas.jsonl')
with open(qnas_filename, 'w') as f:
    json.dump(processed_pages, f)


DATA_PATH = '../../data/Bill_FAQs/parsed'

for n, page in enumerate(processed_pages):
    filename = os.path.join(DATA_PATH, page['title_file'] + '.md')
    print(f"N: {n}, filename: {filename}")

    with open(filename, 'w') as f:
        f.write(page["answer_markdown"])
