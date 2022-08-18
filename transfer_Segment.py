from pathlib import Path
import create_mod_json


def read_text():
    text = Path("annoted_txt.txt").read_text()
    return text


def create_new_segment(text):
    span = []
    prev = 0
    splitted_text = text.split("\n")
    

    for line in splitted_text:
        start = prev
        end = prev+len(line)
        span.append((start,end))
        prev = end
       
    return span


def check_span(spans):
    new_text = ""
    text = Path("བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ་བཞུགས་སོ།.txt").read_text().replace("\n","")
    for span in spans:
        start,end = span
        new_text += text[start:end]+"\n"

    Path("./gen_text.txt").write_text(new_text)

def main():
    text = read_text()
    span = create_new_segment(text)
    create_mod_json.main(span)

if __name__ == "__main__":
    main()