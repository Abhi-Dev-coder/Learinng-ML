from ebooklib import epub
from bs4 import BeautifulSoup
from collections import Counter
import re

# ------------------------
# CONFIG SECTION
# ------------------------
CHARACTER_NAME = "Klein"  # Change this for any character
EPUB_FILE = "lord_of_mysteries.epub"

# ------------------------
# Step 1: Extract all text from EPUB
# ------------------------
def extract_epub_text(file_path):
    book = epub.read_epub(file_path)
    full_text = ""

    for item in book.get_items():
        if item.get_type() == epub.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            full_text += soup.get_text(separator="\n")
    
    return full_text

# ------------------------
# Step 2: Extract lines mentioning the character
# ------------------------
def extract_character_references(text, character):
    lines = text.split("\n")
    related_lines = []

    for line in lines:
        if character.lower() in line.lower():
            related_lines.append(line.strip())

    return related_lines

# ------------------------
# Step 3: Extract direct dialogues
# ------------------------
def extract_dialogues(text):
    dialogues = re.findall(r'\“(.*?)\”', text)
    return dialogues

# ------------------------
# Step 4: Keyword Frequency (tone analysis helper)
# ------------------------
def get_common_keywords(lines, top_n=20):
    words = re.findall(r'\b\w+\b', " ".join(lines).lower())
    stopwords = set(["the", "and", "to", "of", "in", "a", "that", "it", "is", "was", "as", "he", "for", "with", "on", "at", "by", "an", "be", "this", "from"])
    filtered = [w for w in words if w not in stopwords and len(w) > 3]
    return Counter(filtered).most_common(top_n)

# ------------------------
# Step 5: Generate prompt suggestion
# ------------------------
def generate_prompt_template(character_name, keywords):
    prompt = f"""
You are {character_name} from the novel 'Lord of Mysteries'. 
You speak in a composed, mysterious tone, often referring to fate, the occult, and ancient truths. 
You are calm, strategic, and introspective. You do not speak casually and avoid emotional outbursts.
Your language may include terms like:
- {', '.join([kw[0] for kw in keywords[:10]])}

You recall details about The Fool, the Tarot Club, Beyonder Sequences, and your journey. 
Respond like a real person with your own beliefs, not like a robotic assistant.
"""
    return prompt

# ------------------------
# MAIN RUN
# ------------------------
if __name__ == "__main__":
    print("\n[+] Extracting text from EPUB...")
    novel_text = extract_epub_text(EPUB_FILE)

    print("[+] Extracting character-related lines...")
    char_lines = extract_character_references(novel_text, CHARACTER_NAME)

    print("[+] Extracting dialogues...")
    dialogues = extract_dialogues("\n".join(char_lines))

    print("[+] Analyzing keywords...")
    top_keywords = get_common_keywords(char_lines)

    print("\n[+] --- SAMPLE DIALOGUES ---")
    for d in dialogues[:5]:
        print(f"\n- {d}")

    print("\n[+] --- PERSONALITY PROMPT SUGGESTION ---")
    personality_prompt = generate_prompt_template(CHARACTER_NAME, top_keywords)
    print(personality_prompt)

    # ------------------------
    # NEW: Save personality prompt to text file
    # ------------------------
    filename = f"{CHARACTER_NAME.lower()}_personality_prompt.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(personality_prompt)
    print(f"\n[✓] Prompt saved to {filename}")

    print("\n[✓] DONE. You can now copy the prompt into your chatbot code!")
