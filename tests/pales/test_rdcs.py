import pytest
from lib.test_lib import assert_lines_match, isolate_frame, path_in_test_data, clear_cache

from typer.testing import CliRunner
runner = CliRunner()


PALES_TEMPLATE = ['pales', 'export', 'rdcs']
SEQUENCE_STREAM=open(path_in_test_data(__file__, 'pales_test_1.nef', local=True)).read()
SEQUENCE_STREAM_DISORDERED=open(path_in_test_data(__file__, 'pales_test_2.nef', local=True)).read()


@pytest.fixture
def using_pales():
    # register the module under test
    import transcoders.pales

# noinspection PyUnusedLocal
def test_rdcs(typer_app, using_pales, monkeypatch, clear_cache):

    monkeypatch.setattr('sys.stdin.isatty', lambda: False)

    result = runner.invoke(typer_app, [*PALES_TEMPLATE], input=SEQUENCE_STREAM)

    if result.exit_code != 0:
        print('INFO: stdout from failed read:\n', result.stdout)

    assert result.exit_code == 0

    EXPECTED = """\
        REMARK NEF CHAIN A
        REMARK NEF START RESIDUE 1
        
        DATA SEQUENCE AWG
        
        VARS    RESID_I  RESNAME_I  ATOMNAME_I  RESID_J  RESNAME_J  ATOMNAME_J  D      DD     W
        FORMAT  %5d      %6s        %6s         %5d      %6s        %6s         %9.3f  %9.3f  %.2f
                2        TRP        HN          21       TRP        N          -5.2    0.33   1.0
                3        GLY        HN          22       GLY        N           3.1    0.4    1.0

    """

    assert_lines_match (EXPECTED, result.stdout)


# noinspection PyUnusedLocal
def test_rdcs_disordered(typer_app, using_pales, monkeypatch, clear_cache):
    monkeypatch.setattr('sys.stdin.isatty', lambda: False)

    result = runner.invoke(typer_app, [*PALES_TEMPLATE], input=SEQUENCE_STREAM_DISORDERED)

    if result.exit_code != 0:
        print('INFO: stdout from failed read:\n', result.stdout)

    assert result.exit_code == 0

    EXPECTED = """\
        REMARK NEF CHAIN A
        REMARK NEF START RESIDUE 1

        DATA SEQUENCE AWG

        VARS    RESID_I  RESNAME_I  ATOMNAME_I  RESID_J  RESNAME_J  ATOMNAME_J  D      DD     W
        FORMAT  %5d      %6s        %6s         %5d      %6s        %6s         %9.3f  %9.3f  %.2f
                2        TRP        HN          21       TRP        N          -5.2    0.33   1.0
                3        GLY        HN          22       GLY        N           3.1    0.4    1.0

    """

    assert_lines_match(EXPECTED, result.stdout)