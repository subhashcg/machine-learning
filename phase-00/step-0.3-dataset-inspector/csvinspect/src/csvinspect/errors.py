"""Every failure a user can cause, and the message they get for it.

One exception type per thing that can go wrong with the input, all carrying a
message written for the person at the terminal rather than for a traceback.
`cli` catches InspectError and prints `str(e)`; nothing else is caught, so a
genuine bug still produces a real traceback instead of being disguised as bad
input.
"""


class InspectError(Exception):
    """Base for anything wrong with the input file. Message is user-facing."""


class FileProblem(InspectError):
    """Missing, unreadable, empty, or not a file at all."""


class NotTextCSV(InspectError):
    """Binary data: almost certainly the wrong file type (.xlsx, .parquet)."""


class EncodingProblem(InspectError):
    """The bytes are not valid in the chosen encoding. Never silently replaced."""


class MalformedCSV(InspectError):
    """The csv module could not parse the file at all."""
