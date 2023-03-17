import os
import re
import json

def collect_notes():
    json_data_list = []
    for root, dirs, files in os.walk("notes"):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), "r") as f:
                    markdown_text = f.read()
                metadata_regex = r"^---\n(.*?)\n---\n"
                metadata_match = re.search(metadata_regex, markdown_text, re.DOTALL)
                if metadata_match is not None:
                    metadata_str = metadata_match.group(1)
                    metadata = {}
                    for line in metadata_str.split("\n"):
                        key, value = line.split(": ")
                        metadata[key] = value
                else:
                    metadata = {}
                content_regex = r"^#+\s+(.*?)\n([\s\S]*?)(?=\n#|\Z)"
                content_matches = re.findall(content_regex, markdown_text, re.DOTALL | re.MULTILINE)
                content = []
                for match in content_matches:
                    header = match[0]
                    items = match[1]
                    items_list = [i.strip() for i in items.split("- ")[1:]]
                    content.append({
                        "header": header,
                        "items": items_list
                    })
                json_data = {
                    "metadata": metadata,
                    "content": content
                }
                json_data_list.append(json_data)

                # Write the JSON data to a file
    with open('organized_notes.json', 'w') as f:
        json.dump(json_data_list, f, indent=4)

    return json_data_list

notes = collect_notes()