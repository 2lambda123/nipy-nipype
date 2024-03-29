# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from ..whitestripe import WhiteStripe


def test_WhiteStripe_inputs():
    input_map = dict(
        img_type=dict(
            mandatory=False,
        ),
        in_file=dict(
            extensions=None,
            mandatory=True,
        ),
        indices=dict(
            mandatory=False,
        ),
        out_file=dict(
            extensions=None,
            usedefault=True,
        ),
    )
    inputs = WhiteStripe.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(inputs.traits()[key], metakey) == value


def test_WhiteStripe_outputs():
    output_map = dict(
        out_file=dict(
            extensions=None,
        ),
    )
    outputs = WhiteStripe.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            assert getattr(outputs.traits()[key], metakey) == value
