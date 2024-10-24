import re


def clean_document(document):
    # Clean the document text
    document = re.sub(r'^[^\n]*\b[^\s]*\.(?:png|jpg|svg)\b[^\n]{0,50}\n?', '', document, flags=re.MULTILINE)
    # Remove any remaining newlines
    document = re.sub(r'\b(?:https?://[^\s]{1,100})\b\s*$', '', document, flags=re.MULTILINE)
    # Remove any remaining newlines
    document = re.sub(r'\s*\*\s*[^{1,10}]+\s*\n?', '', document)
    # Remove any remaining URLs
    document = re.sub(r'\(\s*(https?://[^\s)]+)\s*\n?\)', '', document)
    # Remove any remaining newlines
    document = re.sub(r'\n\s*\n', '\n', document).strip()
    # Remove any remaining newlines
    document = re.sub(r'\n[^\n]{1,30}\n', '', document)
    # Remove any remaining URLs
    document = re.sub(r'https?://[^\s]+', '', document)
    # Remove any remaining HTML tags
    document = re.sub(r'<[^>]+>', '', document)
    # Remove any remaining special characters
    document = re.sub(r'[^a-zA-Z0-9\s\.,\?!]', '', document)
    # Remove texts like width100 height100 etc., or width="100" height="100", or width: 100px; height: 100px;
    document = re.sub(r'\b(width|height)\s*[:=]?\s*"?\d+(?:px)?\s*"?\s*;?\s*', '', document)
    # Remove texts like 1. A 3. C 5. E (any character followed by a dot followed by a space followed by a character followed by a space)
    document = re.sub(r'\b\d+\.\s*[A-Za-z]\s*', '', document)
    # Remove texts like Skip to site content, Skip directly to content, Skip to main content, etc.
    document = re.sub(r'\bSkip\s+(to\s+|directly\s+to\s+)(site\s+content|main\s+content|search)\s*', '', document, flags=re.IGNORECASE)
    # remove [facebook, twitter, instagram, linkedin, youtube, pinterest, snapchat, reddit, google, amazon, microsoft, apple, wikipedia]
    document = re.sub(r'\b(?:facebook|twitter|instagram|linkedin|youtube|pinterest|snapchat|reddit|google|amazon|microsoft|apple|wikipedia|tiktok)\b', '', document)
    # remove [Facebook, Twitter, Instagram, LinkedIn, YouTube, Pinterest, Snapchat, Reddit, Google, Amazon, Microsoft, Apple, Wikipedia]
    document = re.sub(r'\b(?:Facebook|Twitter|Instagram|LinkedIn|YouTube|Pinterest|Snapchat|Reddit|Google|Amazon|Microsoft|Apple|Wikipedia|TikTok)\b', '', document)
    # remove the Accessibility links|Accessibility|accessibility|Accessibility links
    document = re.sub(r'\bAccessibility links|Accessibility|accessibility|Accessibility links\b', '', document)
    # remove the An official website of the United States government
    document = re.sub(r'\bAn official website of the United States government\b', '', document)
    # remove the Table|table|TABLE|Tables|tables|TABLES number.number pattern
    document = re.sub(r'\bTable|table|TABLE|Tables|tables|TABLES\s+\d+\.\d+\b', '', document)
    # remove the Figure|figure|FIGURE|Figures|figures|FIGURES number.number pattern
    document = re.sub(r'\bFigure|figure|FIGURE|Figures|figures|FIGURES\s+\d+\.\d+\b', '', document)
    # remove the number space number pattern
    document = re.sub(r'\b\d+\s+\d+\b', '', document)
    # remove the number , number pattern
    document = re.sub(r'\b\d+,\d+\b', '', document)
    # remove the number comma number pattern
    document = re.sub(r'\b\d+,\d+\b', '', document)
    # remove the comma comma pattern
    document = re.sub(r',\s*,', '', document)
    # remove the . . pattern
    document = re.sub(r'\.\s*\.', '', document)
    # remove first ", " in the text
    document = re.sub(r'^\s*,\s*', '', document)
    # Remove any remaining extra spaces
    document = re.sub(r'\s+', ' ', document)
    # Remove any remaining newlines
    document = re.sub(r'\n', ' ', document)
    return document
