import markdown
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_markdown(file_path, chunk_size=1000, chunk_overlap=100):
    """Reads a Markdown file, cleans text, and splits it into chunks."""
    
    # Read the Markdown file
    with open(file_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Convert Markdown to HTML (to keep structure)
    html = markdown.markdown(md_text)

    # Use BeautifulSoup to remove HTML tags and get clean text
    text = BeautifulSoup(html, "html.parser").get_text()

    # Initialize a text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    # Create text chunks
    chunks = text_splitter.split_text(text)

    return chunks

# Run the function and get the chunks
chunks = process_markdown("lotm.md")

# Show an example chunk
print(f"Example chunk:\n{chunks[0]}")
