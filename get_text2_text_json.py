from cmath import e
from ctypes import alignment
from distutils.spawn import spawn
import json
from pathlib import Path
from create_opa import from_yaml

def get_alignments(alignment_id):
    opa_dir = "./opa"
    opas = list(Path(opa_dir).iterdir())
    for opa in opas:
        view = get_alignment_pairs(opa,alignment_id)  
        return view  

def get_alignment_pairs(opa,alignment_id):
    alignment_path = Path(f"{opa}/{opa.stem}.opa/Alignment.yml")
    alignments = from_yaml(alignment_path)
    if json_view :=is_alignment_present(alignment_id,alignments):
        return json_view
    return      

def is_alignment_present(alignment_id,alignments):
    seg_pairs = alignments["segment_pairs"]
    segment_sources = alignments["segment_sources"]
    for seg_id in seg_pairs:
        if alignment_id == seg_id:
            seg_pair = seg_pairs[seg_id]
            json_view = get_json_view(seg_pair,seg_id)
            return json_view

def get_json_view(seg_pair,seg_id):
    source_id,target_id = seg_pair.keys()
    source_span = get_span(source_id,seg_pair)
    target_span = get_span(target_id,seg_pair)

    view = {
        "id":seg_id,
        "source":source_id,
        "target":target_id,
        "type":"text",
        "alignments":{
        "source_segment":{
            "start":source_span["start"],
            "end":source_span["end"]
        },
        "target_segment":{
            "start":target_span["start"],
            "end":target_span["end"]
        }
    }
    }

    return view

def get_span(pecha_id,seg_pair):
    opf_dir = "./opf"
    opfs = list(Path(opf_dir).iterdir())
    for opf in opfs:
        if opf.stem == pecha_id:
            if span := retrieve_span(opf,seg_pair,pecha_id):
                return span
    return 

def retrieve_span(opf,seg_pair,pecha_id):
    seg_id = seg_pair[pecha_id]
    layers = get_layers(opf)
    for layer,base_file in layers:
        annotations = layer["annotations"]
        if seg_id not in annotations.keys():
            continue
        else:
            span = annotations[seg_id]["span"]
            #text = get_base_text(span,opf,base_file)
            return span
    return

def get_base_text(span,opf,base_file):
    start,end = span
    base_file_path = f"{opf}/{opf.stem}/{base_file}.txt"
    base_text = Path(base_file_path).read_text()

    return base_text[start:end]


def get_layers(opf):
    layers_path = f"{opf}/{opf.stem}.opf/layers"
    layers = list(Path(layers_path).iterdir())
    for layer in layers:
        segment_yml = from_yaml(Path(layer/"Segment.yml"))
        yield segment_yml,layer.stem

if __name__ == "__main__":
    alignment_id ="de29d0fa5ee64954b2ace4bdc5664eef"
    view = get_alignments(alignment_id)
    print(view)