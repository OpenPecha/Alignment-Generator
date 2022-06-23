from ctypes import alignment
from uuid import uuid4
from pathlib import Path
from openpecha.core.ids import get_alignment_id
import uuid
import yaml

def toyaml(dict):
    return yaml.safe_dump(dict, sort_keys=False, allow_unicode=True)

def from_yaml(yml_path):
    return yaml.safe_load(yml_path.read_text(encoding="utf-8"))

def get_segment_pairs(root_id_segmnt_map,commentary_id_segmnt_map):
    segment_pairs = {}
    root_seg_annotations,root_id = root_id_segmnt_map 
    commentary_seg_annotations,commentary_id = commentary_id_segmnt_map
    for root_seg_id,commentary_seg_id in zip(root_seg_annotations,commentary_seg_annotations):
        root_spans = root_seg_annotations[root_seg_id].span
        commentary_spans = commentary_seg_annotations[commentary_seg_id].span
        segment_pairs.update({uuid4().hex:{
            root_id:root_seg_id,
            commentary_id:commentary_seg_id
        }
        })
    return segment_pairs


def create_opa(root_id_segmnt_map,commentary_id_segmnt_map):
    _,root_id = root_id_segmnt_map 
    _,commentary_id = commentary_id_segmnt_map
    alignment_id = get_alignment_id()
    alignments = {}
    segment_pairs = get_segment_pairs(root_id_segmnt_map,commentary_id_segmnt_map)
    segment_sources = {
        root_id:{
            "type":"origin_type",
            "language":"bo"
        },
        commentary_id:{
            "type":"origin_type",
            "language":"bo"
        }
    }
    alignments.update({"segment_sources":segment_sources})
    alignments.update({"segment_pairs":segment_pairs})
    alignments_yml = toyaml(alignments)
    Path(f"./opa/{alignment_id}/{alignment_id}.opa/").mkdir(parents=True, exist_ok=True)
    Path(f"./opa/{alignment_id}/{alignment_id}.opa/Alignment.yml").write_text(alignments_yml)

    


    

