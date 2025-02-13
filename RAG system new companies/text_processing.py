import re

def remove_html(text):
    """Remove all substrings enclosed in < and > (including self-closing tags)."""
    return re.sub(r'<[^>]*>', '', text)

def is_gibberish(line, threshold=0.3):
    """
    Determine if a line is gibberish.
    A line is considered gibberish if the ratio of alphanumeric characters
    to total characters is below the given threshold.
    """
    stripped_line = line.strip()
    if not stripped_line:
        return False  # keep empty lines or skip further processing if desired
    alnum_count = sum(c.isalnum() for c in stripped_line)
    ratio = alnum_count / len(stripped_line)
    return ratio < threshold

def clean_text(text, gibberish_threshold=0.3):
    # Remove text within angle brackets
    text = remove_html(text)
    # Remove non-ASCII characters (optional)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Split text into lines for further filtering
    lines = text.splitlines()
    filtered_lines = []
    for line in lines:
        if not is_gibberish(line, threshold=gibberish_threshold):
            filtered_lines.append(line.strip())
    return "\n".join(filtered_lines).strip()

def main():
    input_file = 'AMD_Q2 2024.txt'
    output_file = 'AMD_Q2_2024_clean.txt'

    # Read the raw text from the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Clean the text using the enhanced cleaning function
    cleaned_text = clean_text(raw_text, gibberish_threshold=0.3)
    # Write the cleaned text to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

    print(f"Cleaned text has been written to {output_file}")

if __name__ == '__main__':
    main()


