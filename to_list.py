import glob
import os
import re
import pandas as pd
import sys

# Regex patterns
link_pattern = re.compile(r'\[([^\]]+)\]\[(\d+)\]')
ref_pattern = re.compile(r'^\[(\d+)\]:\s*(\S+)', re.MULTILINE)

def extract_links_and_refs(md_text):
    refs = dict(ref_pattern.findall(md_text))
    raw_links = link_pattern.findall(md_text)
    return [(text.strip(), refs[idx]) for text, idx in raw_links if idx in refs]

def collect_all_links(folder):
    records = []
    for path in glob.glob(os.path.join(folder, '*.md')):
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        records.extend(extract_links_and_refs(text))
    return records

def main():
    # Allow folder path from CLI or input
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = input("Enter the path to the folder containing .md files: ").strip()
    
    if not os.path.isdir(folder):
        print(f"❌ Error: '{folder}' is not a valid directory.")
        return

    all_links = collect_all_links(folder)
    unique = sorted(set(all_links), key=lambda x: x[0].lower())

    df = pd.DataFrame(unique, columns=['Link Text', 'Link URL'])
    df.to_csv('all_links.csv', index=False)
    print("✅ Saved: all_links.csv")

    with open('all_links.md', 'w', encoding='utf-8') as f:
        f.write('| Link Text | Link URL |\n|-----------|----------|\n')
        for text, url in unique:
            f.write(f'| {text} | {url} |\n')
    print("✅ Saved: all_links.md")

if __name__ == '__main__':
    main()