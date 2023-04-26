import typer

from nef_pipelines.lib.test_lib import (
    assert_lines_match,
    isolate_loop,
    path_in_test_data,
    run_and_report,
)
from nef_pipelines.transcoders.sparky.importers.sequence import sequence

app = typer.Typer()
app.command()(sequence)

EXPECTED_DNA = """\
  loop_
      _nef_sequence.index
      _nef_sequence.chain_code
      _nef_sequence.sequence_code
      _nef_sequence.residue_name
      _nef_sequence.linking
      _nef_sequence.residue_variant
      _nef_sequence.cis_peptide

     1    A   2    DT   start    .   .
     2    A   3    DG   middle   .   .
     3    A   4    DC   middle   .   .
     4    A   5    DA   middle   .   .
     5    A   6    DT   middle   .   .
     6    A   7    DG   middle   .   .
     7    A   8    DC   middle   .   .
     8    A   9    DA   middle   .   .
     9    A   10   DT   middle   .   .
     10   A   11   DG   middle   .   .
     11   A   12   DC   middle   .   .
     12   A   13   DA   middle   .   .
     13   A   14   DT   middle   .   .
     14   A   15   DG   middle   .   .
     15   A   16   DG   middle   .   .
     16   A   17   DT   middle   .   .
     17   A   18   DG   middle   .   .
     18   A   19   DC   middle   .   .
     19   A   20   DA   middle   .   .
     20   A   21   DT   end      .   .

   stop_
"""


def test_basic_dna():

    sequence_path = path_in_test_data(__file__, "sparky_basic_sequence_dna.txt")

    result = run_and_report(app, ["--molecule-type", "dna", sequence_path])

    assert_lines_match(
        EXPECTED_DNA,
        isolate_loop(result.stdout, "nef_molecular_system", "nef_sequence"),
    )


EXPECTED_PROTEIN = """
   loop_
      _nef_sequence.index
      _nef_sequence.chain_code
      _nef_sequence.sequence_code
      _nef_sequence.residue_name
      _nef_sequence.linking
      _nef_sequence.residue_variant
      _nef_sequence.cis_peptide
     1   A   2   ALA   start    .   .
     2   A   3   CYS   middle   .   .
     3   A   4   ASP   middle   .   .
     4   A   5   GLU   middle   .   .
     5   A   6   PHE   middle   .   .
     6   A   7   GLY   middle   .   .
     7   A   8   HIS   end      .   .
   stop_
"""


def test_basic_protein():

    sequence_path = path_in_test_data(__file__, "sparky_basic_sequence_protein.txt")

    result = run_and_report(app, [sequence_path])

    print(result.stdout)

    assert_lines_match(
        EXPECTED_PROTEIN,
        isolate_loop(result.stdout, "nef_molecular_system", "nef_sequence"),
    )
