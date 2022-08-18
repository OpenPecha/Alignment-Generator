from email.mime import base
from uuid import uuid4
from openpecha.core.pecha import OpenPechaFS
from openpecha.core.metadata import InitialPechaMetadata,InitialCreationType
from openpecha.core.annotation import Page, Span
from openpecha.core.layer import Layer, LayerEnum
from openpecha.core.ids import get_base_id
from pathlib import Path
import re



def get_spans(annoted_text_path):
    char_wlaker = 0
    base_text = ""
    spans = []
    text = Path(annoted_text_path).read_text(encoding="utf-8")
    splitted_text = re.split("endline",text)
    for line in splitted_text:
        spans.append((char_wlaker,char_wlaker+len(line)))
        char_wlaker+=len(line)
        base_text+=line

    return base_text,spans    
      

def create_opf(base_text,spans):
    base_id = get_base_id()
    opf = OpenPechaFS(
        base={base_id:base_text},
        layers=get_layers(base_id,spans),
        meta=get_metadata()
    )
    opf.save(output_path="./opf")

def get_layers(base_id,spans):
    layers = {}
    segmentation_layer = get_segmentation_layers(spans)
    layers[base_id] = {
        LayerEnum.segment : segmentation_layer
    }

    return layers

def get_metadata():
    instance_meta = InitialPechaMetadata(
        initial_creation_type=InitialCreationType.input,
        source="",
        source_metadata= "")
    return instance_meta
    
def get_segmentation_layers(spans):
    segment_annotations = {}
    for span in spans:
        start,end = span
        segment_annotation = {
        uuid4().hex:Page(span=Span(start=start,end=end))}
        segment_annotations.update(segment_annotation)

    segmentation_layer = Layer(
        annotation_type=LayerEnum.segment,annotations=segment_annotations
    ) 
    return segmentation_layer



if __name__ == "__main__":
    annoted_text_path = "annoted_txt.txt"
    base_text,spans = get_spans(annoted_text_path)
    create_opf(base_text,spans)