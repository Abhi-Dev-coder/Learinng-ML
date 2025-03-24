import ebooklib
from ebooklib import epub
import re
import os

def extract_text_from_epub(epub_file):
    """Extracts text content from an EPUB file."""
    book = epub.read_epub(epub_file)
    all_text = []
    for item in book.get_items():
        if item.media_type == 'application/xhtml+xml':
            content = item.get_body_content().decode('utf-8', errors='ignore')  # Handle encoding issues
            all_text.append(content)
    return all_text

def clean_text(html_text):
    """Removes HTML tags and extra whitespace from a string."""
    text = re.sub('<[^<]+?>', ' ', html_text)  # Remove HTML tags
    text = re.sub(r'\n+', '\n', text)         # Remove multiple newlines
    text = re.sub(r'\s+', ' ', text)         # Remove multiple spaces
    return text.strip()

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    """Chunks a large text into smaller, overlapping pieces."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end > len(text):
            end = len(text)
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - chunk_overlap
    return chunks


def save_chunks(chunks, output_dir, filename_prefix="chunk"):
    """Saves the chunks into separate text files in the output directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, chunk in enumerate(chunks):
        filename = os.path.join(output_dir, f"{filename_prefix}_{i:04d}.txt") # use 4 digit zero-padding
        with open(filename, "w", encoding="utf-8") as f:
            f.write(chunk)
    print(f"Saved {len(chunks)} chunks to {output_dir}")

# --- Main Execution ---
if __name__ == "__main__":
    epub_file = "lord_of_mysteries.epub"  # Replace with your EPUB file name
    output_dir = "lom_chunks"  # Directory to save the chunks

    try:
        print(f"Extracting text from {epub_file}...")
        html_contents = extract_text_from_epub(epub_file)

        print("Cleaning the text...")
        cleaned_texts = [clean_text(html) for html in html_contents]

        # Join cleaned texts before chunking, preserving chapter order
        full_text = "\n".join(cleaned_texts)

        print("Chunking the text...")
        chunks = chunk_text(full_text)

        print("Saving the chunks...")
        save_chunks(chunks, output_dir)


        print("Data extraction and preparation complete.")

    except FileNotFoundError:
        print(f"Error: EPUB file '{epub_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
