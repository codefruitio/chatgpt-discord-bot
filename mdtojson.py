import os
import re
import json

def collect_notes():
    # Set the directory to search for Markdown files
    start_dir = 'notes'

    # Create an empty list to store the JSON data for each file
    json_data_list = []

    # Loop over all files in the directory and subdirectories
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            # Check if the file is a Markdown file
            if file.endswith('.md'):
                # Read in the Markdown file
                with open(os.path.join(root, file), 'r') as f:
                    markdown_text = f.read()

                # Extract metadata fields
                metadata_regex = r'^---\n(.*?)\n---\n'
                metadata_match = re.search(metadata_regex, markdown_text, re.DOTALL)
                metadata_str = metadata_match.group(1)
                metadata = {}
                for line in metadata_str.split('\n'):
                    key, value = line.split(': ')
                    metadata[key] = value

                # Extract headers and lists
                content_regex = r'^#+\s+(.*?)\n([\s\S]*?)(?=\n#|\Z)'
                content_matches = re.findall(content_regex, markdown_text, re.DOTALL | re.MULTILINE)
                content = []
                for match in content_matches:
                    header = match[0]
                    items = match[1]
                    items_list = [i.strip() for i in items.split('- ')[1:]]
                    content.append({
                        'header': header,
                        'items': items_list
                    })

                # Combine metadata and content into a dictionary
                json_data = {
                    'metadata': metadata,
                    'content': content
                }

                # Add the JSON data to the list
                json_data_list.append(json_data)

    # Write the JSON data to a file
    with open('organized_notes.json', 'w') as f:
        json.dump(json_data_list, f, indent=4)

    return json_data_list

# Run the function
notes = collect_notes()
