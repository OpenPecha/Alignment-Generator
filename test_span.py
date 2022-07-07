from pathlib import Path

base_text = Path("opf/I4ACC0C26/I4ACC0C26.opf/base/00A0.txt").read_text()

print(base_text[352:499])