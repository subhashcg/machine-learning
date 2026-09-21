"""csvinspect — what is in this CSV, in one streaming pass, standard library only.

    from csvinspect import inspect_file, Options, render
    print(render(inspect_file("data.csv")))
"""

from csvinspect.errors import (
    EncodingProblem,
    FileProblem,
    InspectError,
    MalformedCSV,
    NotTextCSV,
)
from csvinspect.options import Options
from csvinspect.render import render
from csvinspect.report import Report, inspect_file

__all__ = [
    "inspect_file", "render", "Options", "Report",
    "InspectError", "FileProblem", "NotTextCSV", "EncodingProblem", "MalformedCSV",
]
__version__ = "0.1.0"
