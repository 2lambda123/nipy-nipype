# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from __future__ import unicode_literals
from ..utils import ApplyInverseDeformation


def test_ApplyInverseDeformation_inputs():
    input_map = dict(
        bounding_box=dict(field='comp{1}.inv.comp{1}.sn2def.bb', ),
        deformation=dict(
            extensions=None,
            field='comp{1}.inv.comp{1}.sn2def.matname',
            xor=['deformation_field'],
        ),
        deformation_field=dict(
            extensions=None,
            field='comp{1}.inv.comp{1}.def',
            xor=['deformation'],
        ),
        in_files=dict(
            field='fnames',
            mandatory=True,
        ),
        interpolation=dict(field='interp', ),
        matlab_cmd=dict(),
        mfile=dict(usedefault=True, ),
        paths=dict(),
        target=dict(
            extensions=None,
            field='comp{1}.inv.space',
        ),
        use_mcr=dict(),
        use_v8struct=dict(
            min_ver='8',
            usedefault=True,
        ),
        voxel_sizes=dict(field='comp{1}.inv.comp{1}.sn2def.vox', ),
    )
    inputs = ApplyInverseDeformation.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value
def test_ApplyInverseDeformation_outputs():
    output_map = dict(out_files=dict(), )
    outputs = ApplyInverseDeformation.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
