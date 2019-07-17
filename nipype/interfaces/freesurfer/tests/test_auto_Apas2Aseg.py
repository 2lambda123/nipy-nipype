# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..utils import Apas2Aseg


def test_Apas2Aseg_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        in_file=dict(
            argstr='--i %s',
            extensions=None,
            mandatory=True,
        ),
        out_file=dict(
            argstr='--o %s',
            extensions=None,
            mandatory=True,
        ),
        subjects_dir=dict(),
    )
    inputs = Apas2Aseg.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_Apas2Aseg_outputs():
    output_map = dict(
        out_file=dict(
            argstr='%s',
            extensions=None,
        ), )
    outputs = Apas2Aseg.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
