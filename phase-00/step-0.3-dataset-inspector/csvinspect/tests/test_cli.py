"""The command line contract: exit codes, streams, and flags that change answers."""

import pytest

from csvinspect.cli import main


def run(capsys, argv):
    code = main(argv)
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def test_success_prints_a_report_and_exits_zero(write_csv, capsys):
    path = write_csv("id,name\n1,bo\n2,al\n")
    code, out, err = run(capsys, [str(path)])
    assert code == 0 and err == ""
    assert "2 rows × 2 columns" in out
    assert "integer" in out and "text" in out


def test_input_errors_go_to_stderr_with_exit_one(tmp_path, capsys):
    code, out, err = run(capsys, [str(tmp_path / "nope.csv")])
    assert code == 1
    assert out == "", "nothing on stdout: a pipeline must not read an error as data"
    assert err.startswith("error: no such file")


def test_usage_errors_exit_two(capsys):
    with pytest.raises(SystemExit) as excinfo:
        main([])
    assert excinfo.value.code == 2


@pytest.mark.parametrize("bad", [["--limit", "0"], ["--tolerance", "1.5"], ["--bins", "0"]])
def test_impossible_options_are_refused(write_csv, bad, capsys):
    path = write_csv("a\n1\n")
    with pytest.raises(SystemExit) as excinfo:
        main([str(path), *bad])
    assert excinfo.value.code == 2


def test_no_default_na_changes_the_answer(write_csv, capsys):
    path = write_csv("code\nNA\nZW\nUS\n")
    _, default_out, _ = run(capsys, [str(path)])
    assert "1 missing" in default_out, "NA is missing by default"

    _, kept_out, _ = run(capsys, [str(path), "--no-default-na"])
    assert "0 missing" in kept_out, "--no-default-na keeps Namibia"


def test_custom_na_values(write_csv, capsys):
    path = write_csv("x\n1\nUNKNOWN\n3\n")
    _, out, _ = run(capsys, [str(path), "--na-values", "UNKNOWN"])
    assert "integer" in out and "1 missing" in out


def test_limit_is_visible_in_the_output(write_csv, capsys):
    body = "n\n" + "\n".join(str(i) for i in range(1, 101)) + "\n"
    path = write_csv(body)
    _, out, _ = run(capsys, [str(path), "--limit", "5"])
    assert "--limit 5" in out, "a partial report must say it is partial"


def test_version(capsys):
    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])
    assert excinfo.value.code == 0
    assert "0.1.0" in capsys.readouterr().out


def test_help_documents_what_counts_as_missing(capsys):
    with pytest.raises(SystemExit):
        main(["--help"])
    out = capsys.readouterr().out
    assert "n/a" in out and "null" in out, "D1 is a decision; it belongs in --help"
