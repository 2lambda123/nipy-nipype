# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..developer import JistBrainMp2rageSkullStripping


def test_JistBrainMp2rageSkullStripping_inputs():
    input_map = dict(
        args=dict(argstr='%s', ),
        environ=dict(
            nohash=True,
            usedefault=True,
        ),
        inFilter=dict(
            argstr='--inFilter %s',
            extensions=None,
        ),
        inSecond=dict(
            argstr='--inSecond %s',
            extensions=None,
        ),
        inSkip=dict(argstr='--inSkip %s', ),
        inT1=dict(
            argstr='--inT1 %s',
            extensions=None,
        ),
        inT1weighted=dict(
            argstr='--inT1weighted %s',
            extensions=None,
        ),
        null=dict(argstr='--null %s', ),
        outBrain=dict(
            argstr='--outBrain %s',
            hash_files=False,
        ),
        outMasked=dict(
            argstr='--outMasked %s',
            hash_files=False,
        ),
        outMasked2=dict(
            argstr='--outMasked2 %s',
            hash_files=False,
        ),
        outMasked3=dict(
            argstr='--outMasked3 %s',
            hash_files=False,
        ),
        xDefaultMem=dict(argstr='-xDefaultMem %d', ),
        xMaxProcess=dict(
            argstr='-xMaxProcess %d',
            usedefault=True,
        ),
        xPrefExt=dict(argstr='--xPrefExt %s', ),
    )
    inputs = JistBrainMp2rageSkullStripping.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_JistBrainMp2rageSkullStripping_outputs():
    output_map = dict(
        outBrain=dict(extensions=None, ),
        outMasked=dict(extensions=None, ),
        outMasked2=dict(extensions=None, ),
        outMasked3=dict(extensions=None, ),
    )
    outputs = JistBrainMp2rageSkullStripping.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
