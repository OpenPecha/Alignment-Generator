from email.mime import base
from uuid import uuid4
from openpecha.core.pecha import OpenPechaFS
from openpecha.core.metadata import InitialPechaMetadata,InitialCreationType
from openpecha.core.annotation import Page, Span
from openpecha.core.layer import Layer, LayerEnum
from openpecha.core.ids import get_base_id
from pathlib import Path
from create_opa import create_opa
import re

def convert_text_to_list(text):
    text_list = re.split("\n+",text)
    return text_list

def get_text(path):
    with open(path,encoding="utf-8") as f:
        text = f.read()
    text_list = convert_text_to_list(text)
    return text_list

def get_base_text(text_list):
    base_text = ""
    for text in text_list:
        base_text+=text+"\n"

    return base_text[:-1]

def create_opf(text):
    base_id = get_base_id()
    base_text = get_base_text(text)
    layers,segment_annotaions = get_layers(text,base_id)

    opf = OpenPechaFS(
        base= {base_id:base_text},
        layers = layers,
        meta = get_metadata()
    )
    opf_path = opf.save(output_path="./opf")
    print(opf_path)
    return segment_annotaions,opf_path.stem

def get_layers(text,base_id):
    layers = {}
    segmentation_annotaions = {}
    segmentation_layer,segment_annotation = get_segmentation_layers(text)
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

def get_metadata():
    instance_meta = InitialPechaMetadata(
        initial_creation_type=InitialCreationType.input,
        source="",
        source_metadata= "")
    return instance_meta

def is_aligned(text1,text2):
    if len(text1) == len(text2):
        return True
    else:
        return False


def main():
    root_path = "chojuk-alignement/D3874/རྩ་བ།.txt"
    commentary_path = "chojuk-alignement/D3874/འགྲེལ་བ།.txt"
    root_text = get_text(root_path)
    commentary_text = get_text(commentary_path)
    root_id_segmnt_map = create_opf(root_text)
    commentary_id_segmnt_map = create_opf(commentary_text)
    if is_aligned(root_text,commentary_text):
        print("Creating OPA")
        create_opa(root_id_segmnt_map,commentary_id_segmnt_map)

if __name__ == "__main__":
    main()