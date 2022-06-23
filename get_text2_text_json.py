from cmath import e
from ctypes import alignment
from pathlib import Path
from create_opa import from_yaml

def get_alignments(alignment_id):
    opa_dir = "./opa"
    opas = list(Path(opa_dir).iterdir())
    for opa in opas:
        get_alignment_pairs(opa,alignment_id)    

def get_alignment_pairs(opa,alignment_id):
    alignment_path = Path(f"{opa}/{opa.stem}.opa/Alignment.yml")
    alignments = from_yaml(alignment_path)
    is_alignment_present(alignment_id,alignments) 

def is_alignment_present(alignment_id,alignments):
    seg_pairs = alignments["segment_pairs"]
    segment_sources = alignments["segment_sources"]
    for seg_id in seg_pairs:
        if alignment_id == seg_id:
            seg_pair = seg_pairs[seg_id]
            get_json_view(segment_sources,seg_pair,seg_id)

def get_json_view(segment_sources,seg_pair,seg_id):
    source_id,target_id = seg_pair.keys()
    source_text = get_text_from_opf(source_id,seg_pair)
    target_text = get_text_from_opf(target_id,seg_pair)

    alignment = {
        "source_segment":source_text,
        "target_segmenet":target_text
    }

    view = {
        "id":seg_id,
        "source":source_id,
        "target":target_id,
        "type":"text",
        "alignmnets":alignment
    }

    return view

def get_text_from_opf(pecha_id,seg_pair):
    opf_dir = "./opf"
    opfs = list(Path(opf_dir).iterdir())
    for opf in opfs:
        if opf.stem == pecha_id:
            if text := search_text(opf,seg_pair,pecha_id):
                return text
    return 

def search_text(opf,seg_pair,pecha_id):
    seg_id = seg_pair[pecha_id]
    layers = get_layers()
    for layer,base_file in layers:
        annotations = layer["annotations"]
        if seg_id not in annotations.keys():
            continue
        else:
            span = annotations[seg_id]["span"]
            text = get_base_text(span,opf,base_file)
            return text
    return

def get_base_text(span,opf,base_file):
    start,end = span
    base_file_path = f"{opf}/{opf.stem}/{base_file}.txt"
    base_text = Path(base_file_path).read_text()

    return base_text[start:end]


def get_layers(opf):
    layers_path = f"{opf}/layers"
    layers = list(Path(layers_path).iterdir())
    for layer in layers:
        segment_yml = from_yaml(Path(layer/"Segmnet.yml"))
        yield segment_yml,layer.stem

if __name__ == "__main__":
    alignment_id ="1111"
    get_alignments(alignment_id)