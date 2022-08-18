import yaml
import json
from pathlib import Path

def toyaml(dict):
    return yaml.safe_dump(dict, sort_keys=False, allow_unicode=True)

def from_yaml(yml_path):
    return yaml.safe_load(yml_path.read_text(encoding="utf-8"))

def main(root_spans):
    alignments = []
    commentary_layer_path = Path("opf/ID6876F7A/ID6876F7A.opf/layers/7624/Segment.yml")
    commentary_seg_layer = from_yaml(commentary_layer_path)
    commentary_anns = commentary_seg_layer["annotations"]

    for root_span,ann_id in zip(root_spans,commentary_anns):
        comm_span = commentary_anns[ann_id]["span"]
        root_start,root_end = root_span
        root_span = {"start":root_start,"end":root_end}
        alignments.append({
            "source_segment":root_span,
            "target_segment":comm_span
        })


    json_view = {
        "id": "AA0594CC5",
        "source": "O2FCA4A99",
        "target": "ID6876F7A",
        "type": "text",
        "alignment":alignments
        }    

    json_view = json.dumps(json_view)
    Path("./view.json").write_text(json_view)    

def test_json():
    test_text = Path("O2FCA4A99/བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ་བཞུགས་སོ།.txt").read_text()
    json_str = open("view.json").read()
    json_data = json.loads(json_str)
    write_text = ""
    for target_dict in json_data["alignment"]:
        start = target_dict["source_segment"]["start"]
        end = target_dict["source_segment"]["end"]
        write_text+=test_text[start:end]+"\n"
    Path("gen_v1.txt").write_text(write_text)    


if __name__ == "__main__":
    test_json()