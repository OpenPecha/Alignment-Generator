from pathlib import Path

base_text = Path("opf/I8FF172CF/I8FF172CF.opf/base/B2B4.txt").read_text()

print(base_text[88:139])