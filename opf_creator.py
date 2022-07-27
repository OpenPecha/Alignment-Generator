from uuid import uuid4
from openpecha.core.pecha import OpenPechaFS
from openpecha.core.metadata import InitialPechaMetadata,InitialCreationType
from openpecha.core.annotation import Page, Span
from openpecha.core.layer import Layer, LayerEnum
from openpecha.core.ids import get_base_id
from openpecha.core.ids import get_alignment_id
from pathlib import Path
import re
import yaml

def toyaml(dict):
    return yaml.safe_dump(dict, sort_keys=False, allow_unicode=True)

def split_text(path):
    s = open(path, mode='r', encoding='utf-8-sig').read()
    open(path, mode='w', encoding='utf-8').write(s)
    chunk_text = Path(path).read_text()
    splitted_text = re.split("\n",chunk_text)
    cleaned_splitted_text = clean_text(splitted_text)
    return cleaned_splitted_text

def clean_text(lines):
    new_lines = []
    for index,line in enumerate(lines,start=1):
        if index%2 != 0:
            new_lines.append(line.strip())
    return new_lines

def get_base_text(splitted_text):
    base_text = ""
    for line in splitted_text:
        base_text+=line+"\n"
    return base_text

def get_layers(base_text,base_id):
    layers = {}
    segmentation_annotaions = {}
    segmentation_layer,segment_annotation = get_segmentation_layers(base_text)
    layers[base_id] = {
        LayerEnum.segment : segmentation_layer
    }
    segmentation_annotaions.update({base_id:segment_annotation})
    return layers,segment_annotation

def get_segmentation_layers(text_list):
    segment_annotations = {}
    char_walker = 0

    for text in text_list:
        segment_annotation,char_walker = get_segment_annotation(text,char_walker)
        segment_annotations.update(segment_annotation)

    segmentation_layer = Layer(
        annotation_type=LayerEnum.segment,annotations=segment_annotations
    ) 
    return segmentation_layer,segment_annotations

def get_segment_annotation(text,char_walker):
    segment_annotation = {
        uuid4().hex:Page(span=Span(start=char_walker,end=char_walker+len(text)))
    }
    char_walker+=len(text)+1

    return segment_annotation,char_walker


def get_metadata(folder,file):
    main_url="https://github.com/Esukhia/chojuk-alignement/tree/master/"
    instance_meta = InitialPechaMetadata(
        initial_creation_type=InitialCreationType.input,
        source=main_url+folder,
        source_metadata= {
            "title":file
        })
    return instance_meta


def create_opf(splitted_text,folder,file):
    base_id = get_base_id()
    base_text = get_base_text(splitted_text)
    layers,segment_annotaions = get_layers(splitted_text,base_id)
    opf = OpenPechaFS(
        base= {base_id:base_text},
        layers = layers,
        meta = get_metadata(folder,file)
    )
    opf_path = opf.save(output_path="./opf")
    return segment_annotaions,opf_path.stem

def create_opa(**kwargs):
    alignments = {}
    alignment_id = get_alignment_id()
    segment_sources = {
        kwargs["root_id"]:{
            "title":kwargs["root_title"],
            "type":"origin_type",
            "language":"bo"
        },
        kwargs["commentary_id"]:{
            "title":kwargs["commentary_title"],
            "type":"origin_type",
            "language":"bo"
        }
    }
    seg_pairs = get_segment_pairs(**kwargs)
    alignments.update({"segment_sources":segment_sources})
    alignments.update({"segment_pairs":seg_pairs})
    alignments_yml = toyaml(alignments)
    Path(f"./opa/{alignment_id}/{alignment_id}.opa/").mkdir(parents=True, exist_ok=True)
    Path(f"./opa/{alignment_id}/{alignment_id}.opa/Alignment.yml").write_text(alignments_yml)

def get_segment_pairs(**kwargs):
    segment_pairs = {}
    root_annotaions = kwargs["ra"]
    commentary_annotations = kwargs["ca"]
    root_id = kwargs["root_id"]
    commentary_id = kwargs["commentary_id"]
    for root_seg_id,commentary_seg_id in zip(root_annotaions,commentary_annotations):
        segment_pairs.update({uuid4().hex:{
            root_id:root_seg_id,
            commentary_id:commentary_seg_id
        }
        })
    return segment_pairs


def main():
    folder= "D3872-final"
    root_text = "chojuk-alignement/D3872-final/ཐུན་མོང་གི་རྩ་བ།.txt"
    commentary_text = "chojuk-alignement/D3872-final/Commentary.txt"
    splitted_text_root = split_text(root_text)
    splitted_text_commentary = split_text(commentary_text)
    root_annotations,root_id = create_opf(splitted_text_root,folder,Path(root_text).stem)
    commnetary_annotations,commentary_id = create_opf(splitted_text_commentary,folder,Path(commentary_text).stem)
    create_opa(ra = root_annotations,ca = commnetary_annotations,root_title = Path(root_text).stem,commentary_title = Path(commentary_text).stem,root_id = root_id,commentary_id =commentary_id)

if __name__ == "__main__":
    main()