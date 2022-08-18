from antx import transfer
from pathlib import Path


src = Path("I09583FC4/I09583FC4.opf/base/B1B4.txt").read_text()
trg = Path("O2FCA4A99/O2FCA4A99.opf/base/6ABB.txt").read_text()
annotations = [["newline","(endline)"]]
result = transfer(src, annotations, trg, output="txt")
Path("annoted_txt.txt").write_text(result,encoding="utf-8")