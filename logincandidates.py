import re
import csv

def extract_urls_with_regex(input_file, output_csv_path):
    seen=set()
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Regex to match the desired URLs
    regex = r'"login_page_candidate":"(https?://[^"]+)"'
    
    # Find all matches
    matches = re.findall(regex, content)
    
    # Prepare the filtered data
    filtered_data = []
    for idx, url in enumerate(matches, start=1):
        # Remove "https://" or "http://"
        formatted_url = url.replace("https://", "").replace("http://", "")
        if formatted_url in seen:
            continue
        seen.add(formatted_url)
        filtered_data.append({'ID': idx, 'URL': formatted_url})
    
    # Write the filtered data to a new CSV file
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=['ID', 'URL'])
        writer.writeheader()
        writer.writerows(filtered_data)
    
    print(f"Extracted URLs have been saved to {output_csv_path}")

# Example usage
input_file = 'landscape_analysis_tres-3.csv'  # Update with your actual file path
output_csv_path = 'extracted_login_candidates.csv'  # Output file path
extract_urls_with_regex(input_file, output_csv_path)



