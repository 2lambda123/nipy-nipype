"""Autogenerated file - DO NOT EDIT
If you spot a bug, please report it on the mailing list and/or change the generator."""

from nipype.interfaces.base import (
    CommandLine,
    CommandLineInputSpec,
    SEMLikeCommandLine,
    TraitedSpec,
    File,
    Directory,
    traits,
    isdefined,
    InputMultiPath,
    OutputMultiPath,
)
import os


class GenerateAverageLmkFileInputSpec(CommandLineInputSpec):
    inputLandmarkFiles = InputMultiPath(
        traits.Str,
        desc="Input landmark files names (.fcsv or .wts)",
        sep=",",
        argstr="--inputLandmarkFiles %s",
    )
    outputLandmarkFile = traits.Either(
        traits.Bool,
        File(),
        hash_files=False,
        desc="Output landmark file name that includes average values for landmarks (.fcsv or .wts)",
        argstr="--outputLandmarkFile %s",
    )


class GenerateAverageLmkFileOutputSpec(TraitedSpec):
    outputLandmarkFile = File(
        desc="Output landmark file name that includes average values for landmarks (.fcsv or .wts)",
        exists=True,
    )


class GenerateAverageLmkFile(SEMLikeCommandLine):
    """title: Average Fiducials

    category: Testing

    description: This program gets several fcsv file each one contains several landmarks with the same name but slightly different coordinates. For EACH landmark we compute the average coordination.

    contributor: Ali Ghayoor
    """

    input_spec = GenerateAverageLmkFileInputSpec
    output_spec = GenerateAverageLmkFileOutputSpec
    _cmd = " GenerateAverageLmkFile "
    _outputs_filenames = {"outputLandmarkFile": "outputLandmarkFile"}
    _redirect_x = False
