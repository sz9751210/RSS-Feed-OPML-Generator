import xml.etree.ElementTree as ET
import requests
import logging
import urllib3
from urllib3.exceptions import InsecureRequestWarning

def parse_markdown(markdown_text):
    lines = markdown_text.split('\n')
    categories = []
    current_category = None

    for line in lines:
        # Check if the line is a heading
        if line.startswith('#'):
            # Determine the heading level (1 to 6)
            heading_level = len(line.split(' ')[0])
            if 1 <= heading_level <= 6:
                if current_category:
                    categories.append(current_category)
                current_category = {'title': line.strip('# ').strip(), 'links': []}
        elif line.startswith('- ['):  # Link line
            if current_category is not None:
                parts = line.split('](')
                title = parts[0][3:].strip()
                url = parts[1][:-1].strip()
                current_category['links'].append({'title': title, 'url': url})

    if current_category:
        categories.append(current_category)

    return categories


def check_url_exists(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10, verify=False, allow_redirects=False)
        logging.info(f"Checking URL: {url} - Status Code: {response.status_code}")
        # print(f"Checking URL: {url} - Status Code: {response.status_code}")
        return response.status_code == 200
    except requests.RequestException as e:
        logging.error(f"Error checking URL: {url} - Error: {e}")
        # print(f"Error checking URL: {url} - Error: {e}")
        return False


def find_rss_link(base_url):
    rss_variants = [
        "/rss", "/rss.xml", "/index.xml", "/atom.xml",
        "/feed", "/feeds/posts/default", "/feed/rss", 
        "/feed/rss2", "/feed/atom", "/?feed=rss", 
        "/?feed=rss2", "/?feed=atom"
    ]
    for variant in rss_variants:
        full_url = base_url.rstrip('/') + variant
        if check_url_exists(full_url):
            return full_url
    return None


def generate_opml(categories):
    opml = ET.Element("opml", version="2.0")
    head = ET.SubElement(opml, "head")
    ET.SubElement(head, "title").text = "Feeds"
    body = ET.SubElement(opml, "body")

    for category in categories:
        outline = ET.SubElement(body, "outline", text=category['title'], title=category['title'])
        for link in category['links']:
            rss_link = find_rss_link(link['url'])
            if rss_link:
                ET.SubElement(outline, "outline", type="rss", htmlUrl=link['url'], xmlUrl=rss_link, title=link['title'], text=link['title'])

    return ET.tostring(opml, encoding="unicode")

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


def main():
    logging.basicConfig(level=logging.INFO)
    markdown_file_path = 'rss.md'
    output_filename = "output.opml"
    urllib3.disable_warnings(InsecureRequestWarning)
    markdown_content = read_markdown_file(markdown_file_path)
    categories = parse_markdown(markdown_content)
    opml_output = generate_opml(categories)
    write_to_file(output_filename, opml_output)
    print(f"OPML output written to {output_filename}")

if __name__ == "__main__":
    main()
