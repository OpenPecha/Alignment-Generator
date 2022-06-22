from uuid import uuid4
from openpecha.core.pecha import OpenPechaFS
from openpecha.core.metadata import InitialPechaMetadata,InitialCreationType
from openpecha.core.annotation import Page, Span
from openpecha.core.layer import Layer, LayerEnum
from openpecha import github_utils
from openpecha.core.ids import get_initial_pecha_id,get_base_id
from pathlib import Path
from bs4 import BeautifulSoup
from pyparsing import col
import requests
import os
import re
import logging



def convert_text_to_list(text):
    text_list = text.split("\n\n")
    return text_list

def get_text(path):
    text = Path(path).read_text()
    return text

def create_opf(text):
    base_id = get_base_id()
    opf = OpenPechaFS(
        base= {base_id:text},
        layers = get_layers(text,base_id),
        meta = get_metadata()
    )
    opf.save(output_path="./root")

def get_layers(text,base_id):
    layers = {}
    layers[base_id] = {
        LayerEnum.segment : get_segmentation_layers(text)
    }
    return layers

def get_segmentation_layers(text):
    segment_annotations = {}
    char_walker = 0
    text_list = convert_text_to_list(text)

    for text in text_list:
        segment_annotation,char_walker = get_segment_annotation(text,char_walker)
        segment_annotations.update(segment_annotation)

    segmentation_layer = Layer(
        annotation_type=LayerEnum.segment,annotations=segment_annotations
    ) 
    return segmentation_layer

def get_segment_annotation(text,char_walker):
    segment_annotation = {
        uuid4().hex:Page(span=Span(start=char_walker,end=char_walker+len(text)))
    }
    char_walker+=len(text)+2

    return segment_annotation,char_walker

def get_metadata():
    instance_meta = InitialPechaMetadata(
        initial_creation_type=InitialCreationType.input,
        source="",
        source_metadata= "")
    return instance_meta

def is_aligned(text1,text2):
    text1_list = convert_text_to_list(text1)
    text2_list = convert_text_to_list(text2)

    if len(text1_list) == len(text2_list):
        return True
    else:
        return False


def main():
    root_path = "chojuk-alignement/Tupten Choedak/Root1.txt"
    commentary_path = "chojuk-alignement/Tupten Choedak/Description1.txt"
    root_text = get_text(root_path)
    commentary_text = get_text(commentary_path)
    create_opf(root_text)
    create_opf(commentary_text)
    if is_aligned(root_text,commentary_text):
        print("Creating OPA")
        

if __name__ == "__main__":
    main()