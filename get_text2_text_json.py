from cmath import e
from ctypes import alignment
from distutils.spawn import spawn
import json
from pathlib import Path
from create_opa import from_yaml, toyaml

def get_alignments(alignment_id):
    opa_dir = "./root/opas"
    opas = list(Path(opa_dir).iterdir())
    for opa in opas:
        view = get_alignment_pairs(opa,alignment_id)  
        return view  

def get_alignment_pairs(opa,alignment_id):
    bases = list(Path(f"{opa}/{opa.stem}.opa").iterdir())

    for base in bases:
        alignment_path = Path(f"{base}/Alignment.yml")
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
    alignments = {}
    view = {
        "id":seg_id,
        "type":"text"
    }
    for id in seg_pair.keys():
        source_span = get_span(id,seg_pair)
        alignment = {
            seg_pair[id]:{
                "start":source_span[0],
                "end":source_span[1]
            }}
        alignments.update(alignment)
    view["alignment"] =  alignments

    return view

def get_span(pecha_id,seg_pair):
    opf_dir = "./root/opfs"
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
            text = get_base_text(span,opf,base_file)
            return [text,text]
    return

def get_base_text(span,opf,base_file):
    start= span["start"]
    end = span["end"]
    base_file_path = f"{opf}/{opf.stem}.opf/base/{base_file}.txt"
    base_text = Path(base_file_path).read_text()
    print(base_file_path)
    return base_text[start:end]


def get_layers(opf):
    layers_path = f"{opf}/{opf.stem}.opf/layers"
    layers = list(Path(layers_path).iterdir())
    for layer in layers:
        segment_yml = from_yaml(Path(layer/"Segment.yml"))
        yield segment_yml,layer.stem

def get_alignment_chojuk(alignment):
    segment_sources = alignment["segment_sources"].keys()
    source,target = segment_sources
    seg_pairs = alignment["segment_pairs"]
    alignments = []
    for alignent_id in seg_pairs:
        print(alignent_id)
        source_seg_id = seg_pairs[alignent_id][source]
        target_seg_id = seg_pairs[alignent_id][target]
        source_span = get_span(source_seg_id,source)
        target_span  =get_span(target_seg_id,target)
        alignments.append({
            "source_segment":source_span,
            "target_segment":target_span
        })
    json_view = {
        "id": "A48897657",
        "source": source_seg_id,
        "target": target_seg_id,
        "type": "text",
        "alignment":alignments
        }    

    return json_view    

def get_span(seg_id,pecha_id):
    segment_layer_paths = list(Path(f"./opf/{pecha_id}/{pecha_id}.opf/layers").iterdir())
    for segment_layer_path in segment_layer_paths:
        segment_layer = from_yaml(Path(segment_layer_path / "Segment.yml"))
        if span := check_span(segment_layer,seg_id):
            return span

def check_span(segment_layer,seg_id):
    annotations = segment_layer["annotations"]
    if seg_id in annotations.keys():
        span = annotations[seg_id]["span"]
        return span
    return 

def main():
    alignment = from_yaml(Path("opa/A48897657/A48897657.opa/Alignment.yml"))
    json_view = get_alignment_chojuk(alignment)
    json_view = json.dumps(json_view)
    Path("./view.json").write_text(json_view)

if __name__ == "__main__":
    main()
    """ alignment_path = "opa/A48897657/A48897657.opa/Alignment.yml"
    alignments = from_yaml(Path(alignment_path))
    view = get_alignments(alignments)
    print(view) """