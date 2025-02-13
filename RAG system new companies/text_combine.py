import os

def combine_text_files(input_folder, output_file):
    """
    Combines all .txt files in the given input_folder into a single output_file.
    For each file, writes a header line containing the file name as a key ID,
    then the content of the file, and a separator line.
    """
    # List all files in the folder and sort them if needed
    files = sorted(f for f in os.listdir(input_folder) if f.endswith('.txt'))
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in files:
            filepath = os.path.join(input_folder, filename)
            with open(filepath, 'r', encoding='utf-8') as infile:
                content = infile.read().strip()
            
            # Write the header (key id and file name)
            outfile.write(f"ID: {filename}\n")
            # Write the file's content
            outfile.write(content + "\n")
            # Write a separator between entries (optional)
            outfile.write("\n" + "=" * 50 + "\n\n")

if __name__ == '__main__':
    # Set the path to the folder containing the text files
    input_folder = r'C:\Users\palas\Desktop\AIP\extracted_sec_text'  # update with your folder path
    # Set the name of the combined output file
    output_file = 'combined_document.txt'
    
    combine_text_files(input_folder, output_file)
    print(f"Combined file created: {output_file}")
