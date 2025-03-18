import csv

def load_domains(file_path):
    """Loads the domains from the first file, ignoring the numerical prefixes."""
    domains = set()
    with open(file_path, 'r') as file:
        for line in file:
            _, domain = line.strip().split(',')
            domains.add(domain)
    return domains

def filter_file(input_file, output_file, allowed_domains):
    """Filters the input file and writes only matching rows to the output file."""
    with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Write the header
        header = next(reader)
        writer.writerow(header)
        
        for row in reader:
            domain = row[0].replace('www.', '')  # Remove 'www.' prefix if present
            shouldWrite=False
            for curr_domain in allowed_domains:
                if curr_domain == domain:
                    print(curr_domain, row[0])
                    shouldWrite=True
                    break
            if shouldWrite:
                writer.writerow(row)

def main():
    domains_file = 'tmp.csv'  # Update with actual filename
    input_file = 'results/predictions_20k.csv'  # Update with actual filename
    output_file = 'filtered_data.csv'  # Output filename

    allowed_domains = load_domains(domains_file)
    print(allowed_domains)
    print(len(allowed_domains))
    filter_file(input_file, output_file, allowed_domains)
    print("Filtering complete. Output saved to", output_file)

if __name__ == "__main__":
    main()