# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
import os
import warnings

import pytest

from ....utils.filemanip import split_filename
from ... import base as nib
from ...base import traits, Undefined
from ....interfaces import fsl
from ...utility.wrappers import Function
from ....pipeline import Node
from ..specs import get_filecopy_info


@pytest.fixture(scope="module")
def setup_file(request, tmpdir_factory):
    tmp_dir = tmpdir_factory.mktemp("files")
    tmp_infile = tmp_dir.join("foo.txt")
    with tmp_infile.open("w") as fp:
        fp.writelines(["123456789"])

    tmp_dir.chdir()

    return tmp_infile.strpath


def test_TraitedSpec():
    assert nib.TraitedSpec().get_hashval()
    assert nib.TraitedSpec().__repr__() == "\n\n"

    class spec(nib.TraitedSpec):
        foo = nib.traits.Int
        goo = nib.traits.Float(usedefault=True)

    assert spec().foo == Undefined
    assert spec().goo == 0.0
    specfunc = lambda x: spec(hoo=x)
    with pytest.raises(nib.traits.TraitError):
        specfunc(1)
    infields = spec(foo=1)
    hashval = (
        [("foo", 1), ("goo", "0.0000000000")],
        "e89433b8c9141aa0fda2f8f4d662c047",
    )
    assert infields.get_hashval() == hashval
    assert infields.__repr__() == "\nfoo = 1\ngoo = 0.0\n"


def test_TraitedSpec_tab_completion():
    bet_nd = Node(fsl.BET(), name="bet")
    bet_interface = fsl.BET()
    bet_inputs = bet_nd.inputs.class_editable_traits()
    bet_outputs = bet_nd.outputs.class_editable_traits()

    # Check __all__ for bet node and interface inputs
    assert set(bet_nd.inputs.__all__) == set(bet_inputs)
    assert set(bet_interface.inputs.__all__) == set(bet_inputs)

    # Check __all__ for bet node outputs
    assert set(bet_nd.outputs.__all__) == set(bet_outputs)


@pytest.mark.skip
def test_TraitedSpec_dynamic():
    from pickle import dumps, loads

    a = nib.BaseTraitedSpec()
    a.add_trait("foo", nib.traits.Int)
    a.foo = 1
    assign_a = lambda: setattr(a, "foo", "a")
    with pytest.raises(Exception):
        assign_a
    pkld_a = dumps(a)
    unpkld_a = loads(pkld_a)
    assign_a_again = lambda: setattr(unpkld_a, "foo", "a")
    with pytest.raises(Exception):
        assign_a_again


def test_DynamicTraitedSpec_tab_completion():
    def extract_func(list_out):
        return list_out[0]

    # Define interface
    func_interface = Function(
        input_names=["list_out"],
        output_names=["out_file", "another_file"],
        function=extract_func,
    )
    # Define node
    list_extract = Node(
        Function(
            input_names=["list_out"], output_names=["out_file"], function=extract_func
        ),
        name="list_extract",
    )

    # Check __all__ for interface inputs
    expected_input = set(list_extract.inputs.editable_traits())
    assert set(func_interface.inputs.__all__) == expected_input

    # Check __all__ for node inputs
    assert set(list_extract.inputs.__all__) == expected_input

    # Check __all__ for node outputs
    expected_output = set(list_extract.outputs.editable_traits())
    assert set(list_extract.outputs.__all__) == expected_output

    # Add trait and retest
    list_extract._interface._output_names.append("added_out_trait")
    expected_output.add("added_out_trait")
    assert set(list_extract.outputs.__all__) == expected_output


def test_TraitedSpec_logic():
    class spec3(nib.TraitedSpec):
        _xor_inputs = ("foo", "bar")

        foo = nib.traits.Int(xor=_xor_inputs, desc="foo or bar, not both")
        bar = nib.traits.Int(xor=_xor_inputs, desc="bar or foo, not both")
        kung = nib.traits.Float(requires=("foo",), position=0, desc="kung foo")

    class out3(nib.TraitedSpec):
        output = nib.traits.Int

    class MyInterface(nib.BaseInterface):
        input_spec = spec3
        output_spec = out3

    myif = MyInterface()
    # NOTE_dj, FAIL: I don't get a TypeError, only a UserWarning
    # with pytest.raises(TypeError):
    #     setattr(myif.inputs, 'kung', 10.0)
    myif.inputs.foo = 1
    assert myif.inputs.foo == 1
    set_bar = lambda: setattr(myif.inputs, "bar", 1)
    with pytest.raises(IOError):
        set_bar()
    assert myif.inputs.foo == 1
    myif.inputs.kung = 2
    assert myif.inputs.kung == 2.0


def test_deprecation():
    with warnings.catch_warnings(record=True) as w:
        warnings.filterwarnings("always", "", UserWarning)

        class DeprecationSpec1(nib.TraitedSpec):
            foo = nib.traits.Int(deprecated="0.1")

        spec_instance = DeprecationSpec1()
        set_foo = lambda: setattr(spec_instance, "foo", 1)
        with pytest.raises(nib.TraitError):
            set_foo()
        assert len(w) == 0, "no warnings, just errors"

    with warnings.catch_warnings(record=True) as w:
        warnings.filterwarnings("always", "", UserWarning)

        class DeprecationSpec2(nib.TraitedSpec):
            foo = nib.traits.Int(deprecated="100", new_name="bar")

        spec_instance = DeprecationSpec2()
        set_foo = lambda: setattr(spec_instance, "foo", 1)
        with pytest.raises(nib.TraitError):
            set_foo()
        assert len(w) == 0, "no warnings, just errors"

    with warnings.catch_warnings(record=True) as w:
        warnings.filterwarnings("always", "", UserWarning)

        class DeprecationSpec3(nib.TraitedSpec):
            foo = nib.traits.Int(deprecated="1000", new_name="bar")
            bar = nib.traits.Int()

        spec_instance = DeprecationSpec3()
        not_raised = True
        try:
            spec_instance.foo = 1
        except nib.TraitError:
            not_raised = False
        assert not_raised
        assert len(w) == 1, f"deprecated warning 1 {[str(w1) for w1 in w]}"

    with warnings.catch_warnings(record=True) as w:
        warnings.filterwarnings("always", "", UserWarning)

        class DeprecationSpec3(nib.TraitedSpec):
            foo = nib.traits.Int(deprecated="1000", new_name="bar")
            bar = nib.traits.Int()

        spec_instance = DeprecationSpec3()
        not_raised = True
        try:
            spec_instance.foo = 1
        except nib.TraitError:
            not_raised = False
        assert not_raised
        assert spec_instance.foo == Undefined
        assert spec_instance.bar == 1
        assert len(w) == 1, f"deprecated warning 2 {[str(w1) for w1 in w]}"


def test_namesource(setup_file):
    tmp_infile = setup_file
    tmpd, nme, ext = split_filename(tmp_infile)

    class spec2(nib.CommandLineInputSpec):
        moo = nib.File(name_source=["doo"], hash_files=False, argstr="%s", position=2)
        doo = nib.File(exists=True, argstr="%s", position=1)
        goo = traits.Int(argstr="%d", position=4)
        poo = nib.File(name_source=["goo"], hash_files=False, argstr="%s", position=3)

    class TestName(nib.CommandLine):
        _cmd = "mycommand"
        input_spec = spec2

    testobj = TestName()
    testobj.inputs.doo = tmp_infile
    testobj.inputs.goo = 99
    assert "%s_generated" % nme in testobj.cmdline
    assert "%d_generated" % testobj.inputs.goo in testobj.cmdline
    testobj.inputs.moo = "my_%s_template"
    assert "my_%s_template" % nme in testobj.cmdline


def test_chained_namesource(setup_file):
    tmp_infile = setup_file
    tmpd, nme, ext = split_filename(tmp_infile)

    class spec2(nib.CommandLineInputSpec):
        doo = nib.File(exists=True, argstr="%s", position=1)
        moo = nib.File(
            name_source=["doo"],
            hash_files=False,
            argstr="%s",
            position=2,
            name_template="%s_mootpl",
        )
        poo = nib.File(name_source=["moo"], hash_files=False, argstr="%s", position=3)

    class TestName(nib.CommandLine):
        _cmd = "mycommand"
        input_spec = spec2

    testobj = TestName()
    testobj.inputs.doo = tmp_infile
    res = testobj.cmdline
    assert "%s" % tmp_infile in res
    assert "%s_mootpl " % nme in res
    assert "%s_mootpl_generated" % nme in res


def test_cycle_namesource1(setup_file):
    tmp_infile = setup_file
    tmpd, nme, ext = split_filename(tmp_infile)

    class spec3(nib.CommandLineInputSpec):
        moo = nib.File(
            name_source=["doo"],
            hash_files=False,
            argstr="%s",
            position=1,
            name_template="%s_mootpl",
        )
        poo = nib.File(name_source=["moo"], hash_files=False, argstr="%s", position=2)
        doo = nib.File(name_source=["poo"], hash_files=False, argstr="%s", position=3)

    class TestCycle(nib.CommandLine):
        _cmd = "mycommand"
        input_spec = spec3

    # Check that an exception is raised
    to0 = TestCycle()
    not_raised = True
    try:
        to0.cmdline
    except nib.NipypeInterfaceError:
        not_raised = False
    assert not not_raised


def test_cycle_namesource2(setup_file):
    tmp_infile = setup_file
    tmpd, nme, ext = split_filename(tmp_infile)

    class spec3(nib.CommandLineInputSpec):
        moo = nib.File(
            name_source=["doo"],
            hash_files=False,
            argstr="%s",
            position=1,
            name_template="%s_mootpl",
        )
        poo = nib.File(name_source=["moo"], hash_files=False, argstr="%s", position=2)
        doo = nib.File(name_source=["poo"], hash_files=False, argstr="%s", position=3)

    class TestCycle(nib.CommandLine):
        _cmd = "mycommand"
        input_spec = spec3

    # Check that loop can be broken by setting one of the inputs
    to1 = TestCycle()
    to1.inputs.poo = tmp_infile

    not_raised = True
    try:
        res = to1.cmdline
    except nib.NipypeInterfaceError:
        not_raised = False
    print(res)

    assert not_raised
    assert "%s" % tmp_infile in res
    assert "%s_generated" % nme in res
    assert "%s_generated_mootpl" % nme in res


def test_namesource_constraints(setup_file):
    tmp_infile = setup_file
    tmpd, nme, ext = split_filename(tmp_infile)

    class constrained_spec(nib.CommandLineInputSpec):
        in_file = nib.File(argstr="%s", position=1)
        threshold = traits.Float(argstr="%g", xor=["mask_file"], position=2)
        mask_file = nib.File(
            argstr="%s",
            name_source=["in_file"],
            name_template="%s_mask",
            keep_extension=True,
            xor=["threshold"],
            position=2,
        )
        out_file1 = nib.File(
            argstr="%s",
            name_source=["in_file"],
            name_template="%s_out1",
            keep_extension=True,
            position=3,
        )
        out_file2 = nib.File(
            argstr="%s",
            name_source=["in_file"],
            name_template="%s_out2",
            keep_extension=True,
            requires=["threshold"],
            position=4,
        )

    class TestConstrained(nib.CommandLine):
        _cmd = "mycommand"
        input_spec = constrained_spec

    tc = TestConstrained()

    # name_source undefined, so template traits remain undefined
    assert tc.cmdline == "mycommand"

    # mask_file and out_file1 enabled by name_source definition
    tc.inputs.in_file = os.path.basename(tmp_infile)
    assert tc.cmdline == "mycommand foo.txt foo_mask.txt foo_out1.txt"

    # mask_file disabled by threshold, out_file2 enabled by threshold
    tc.inputs.threshold = 10.0
    assert tc.cmdline == "mycommand foo.txt 10 foo_out1.txt foo_out2.txt"


def test_TraitedSpec_withFile(setup_file):
    tmp_infile = setup_file
    tmpd, nme = os.path.split(tmp_infile)
    assert os.path.exists(tmp_infile)

    class spec2(nib.TraitedSpec):
        moo = nib.File(exists=True)
        doo = nib.traits.List(nib.File(exists=True))

    infields = spec2(moo=tmp_infile, doo=[tmp_infile])
    hashval = infields.get_hashval(hash_method="content")
    assert hashval[1] == "a00e9ee24f5bfa9545a515b7a759886b"


def test_TraitedSpec_withNoFileHashing(setup_file):
    tmp_infile = setup_file
    tmpd, nme = os.path.split(tmp_infile)
    assert os.path.exists(tmp_infile)

    class spec2(nib.TraitedSpec):
        moo = nib.File(exists=True, hash_files=False)
        doo = nib.traits.List(nib.File(exists=True))

    infields = spec2(moo=nme, doo=[tmp_infile])
    hashval = infields.get_hashval(hash_method="content")
    assert hashval[1] == "8da4669ff5d72f670a46ea3e7a203215"

    class spec3(nib.TraitedSpec):
        moo = nib.File(exists=True, name_source="doo")
        doo = nib.traits.List(nib.File(exists=True))

    infields = spec3(moo=nme, doo=[tmp_infile])
    hashval1 = infields.get_hashval(hash_method="content")

    class spec4(nib.TraitedSpec):
        moo = nib.File(exists=True)
        doo = nib.traits.List(nib.File(exists=True))

    infields = spec4(moo=nme, doo=[tmp_infile])
    hashval2 = infields.get_hashval(hash_method="content")
    assert hashval1[1] != hashval2[1]


def test_ImageFile():
    x = nib.BaseInterface().inputs

    # setup traits
    x.add_trait("nifti", nib.ImageFile(types=["nifti1", "dicom"]))
    x.add_trait("anytype", nib.ImageFile())
    with pytest.raises(ValueError):
        x.add_trait("newtype", nib.ImageFile(types=["nifti10"]))
    x.add_trait("nocompress", nib.ImageFile(types=["mgh"], allow_compressed=False))

    with pytest.raises(nib.TraitError):
        x.nifti = "test.mgz"
    x.nifti = "test.nii"
    x.anytype = "test.xml"
    with pytest.raises(nib.TraitError):
        x.nocompress = "test.mgz"
    x.nocompress = "test.mgh"


def test_filecopy_info():
    class InputSpec(nib.TraitedSpec):
        foo = nib.traits.Int(desc="a random int")
        goo = nib.traits.Int(desc="a random int", mandatory=True)
        moo = nib.traits.Int(desc="a random int", mandatory=False)
        hoo = nib.traits.Int(desc="a random int", usedefault=True)
        zoo = nib.File(desc="a file", copyfile=False)
        woo = nib.File(desc="a file", copyfile=True)

    class DerivedInterface(nib.BaseInterface):
        input_spec = InputSpec
        resource_monitor = False

        def normalize_filenames(self):
            """A mock normalize_filenames for freesurfer interfaces that have one"""
            self.inputs.zoo = "normalized_filename.ext"

    assert get_filecopy_info(nib.BaseInterface) == []

    # Test on interface class, not instantiated
    info = get_filecopy_info(DerivedInterface)
    assert info[0]["key"] == "woo"
    assert info[0]["copy"]
    assert info[1]["key"] == "zoo"
    assert not info[1]["copy"]
    info = None

    # Test with instantiated interface
    derived = DerivedInterface()
    # First check that zoo is not defined
    assert derived.inputs.zoo == Undefined
    # After the first call to get_filecopy_info zoo is defined
    info = get_filecopy_info(derived)
    # Ensure that normalize_filenames was called
    assert derived.inputs.zoo == "normalized_filename.ext"
    # Check the results are consistent
    assert info[0]["key"] == "woo"
    assert info[0]["copy"]
    assert info[1]["key"] == "zoo"
    assert not info[1]["copy"]
