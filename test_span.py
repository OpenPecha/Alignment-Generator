from pathlib import Path
from create_mod_json import toyaml,from_yaml

base_text = Path("opf/IE50A844F/IE50A844F.opf/base/C534.txt").read_text(encoding="utf-8")
layer_path = Path("opf/IE50A844F/IE50A844F.opf/layers/C534/Segment.yml")
ann = from_yaml(layer_path)

annotations = ann['annotations']
new_base_text = ""
for seg_id in annotations:
    span = annotations[seg_id]["span"]
    start = span["start"]
    end = span["end"]
    new_base_text+=base_text[start:end].replace("\n","")+"\n"

Path("test_base_text.txt").write_text(new_base_text)

