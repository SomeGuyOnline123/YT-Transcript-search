import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

def extract_youtube_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    urls = []

    # Find all anchor tags in the HTML content
    anchor_tags = soup.find_all('a')

    # Extract YouTube URLs from anchor tags
    for tag in anchor_tags:
        url = tag.get('href')
        if url and 'youtube.com' in url:
            # Parse the URL
            parsed_url = urlparse(url)

            # Extract and keep only the 'v' parameter
            query_parameters = parse_qs(parsed_url.query)
            v_parameter = query_parameters.get('v')
            if v_parameter:
                query = urlencode({'v': v_parameter[0]})
            else:
                query = ''

            # Reconstruct the URL with only the 'v' parameter
            clean_url = urlunparse(parsed_url._replace(query=query))

            urls.append(clean_url)

    return urls

# Directory containing HTML files
directory = 'episodes'

# Set to store unique YouTube URLs
unique_urls = set()

# Loop through HTML files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        # Read HTML file
        with open(os.path.join(directory, filename), 'r') as file:
            html_content = file.read()

        # Extract YouTube URLs from HTML
        urls = extract_youtube_urls(html_content)

        # Add URLs to the set
        unique_urls.update(urls)

# Print the unique YouTube URLs
for url in unique_urls:
    print(url)
