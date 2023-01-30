import typer

from nef_pipelines.lib.test_lib import (
    assert_lines_match,
    isolate_frame,
    path_in_test_data,
    run_and_report,
)
from nef_pipelines.transcoders.csv.importers.rdcs import rdcs

app = typer.Typer()
app.command()(rdcs)


# noinspection PyUnusedLocal
def test_short_csv():
    sequence_path = path_in_test_data(__file__, "3a_ab.neff")
    csv_path = path_in_test_data(__file__, "short.csv")

    nef_sequence = open(sequence_path, "r").read()

    args = [csv_path]
    result = run_and_report(app, args, input=nef_sequence)

    EXPECTED = """\
        save_nef_rdc_restraint_list_rdcs
           _nef_rdc_restraint_list.sf_category           nef_rdc_restraint_list
           _nef_rdc_restraint_list.sf_framecode          nef_rdc_restraint_list_rdcs
           _nef_rdc_restraint_list.restraint_origin      .
           _nef_rdc_restraint_list.tensor_magnitude      .
           _nef_rdc_restraint_list.tensor_rhombicity     .
           _nef_rdc_restraint_list.tensor_chain_code     .
           _nef_rdc_restraint_list.tensor_sequence_code  .
           _nef_rdc_restraint_list.tensor_residue_name   .

           loop_
              _nef_rdc_restraint.index
              _nef_rdc_restraint.restraint_id
              _nef_rdc_restraint.restraint_combination_id
              _nef_rdc_restraint.chain_code_1
              _nef_rdc_restraint.sequence_code_1
              _nef_rdc_restraint.residue_name_1
              _nef_rdc_restraint.atom_name_1
              _nef_rdc_restraint.chain_code_2
              _nef_rdc_restraint.sequence_code_2
              _nef_rdc_restraint.residue_name_2
              _nef_rdc_restraint.atom_name_2
              _nef_rdc_restraint.weight
              _nef_rdc_restraint.target_value
              _nef_rdc_restraint.target_value_uncertainty
              _nef_rdc_restraint.lower_linear_limit
              _nef_rdc_restraint.lower_limit
              _nef_rdc_restraint.upper_limit
              _nef_rdc_restraint.upper_linear_limit
              _nef_rdc_restraint.scale
              _nef_rdc_restraint.distance_dependent

             0   0   .   A   11   .   H   A   11   .   N   1.0   1.3   .   .   .   .   .   1.0   .
             1   1   .   A   12   .   H   A   12   .   N   1.0   4.6   .   .   .   .   .   1.0   .
             2   2   .   A   13   .   H   A   13   .   N   1.0   2.4   .   .   .   .   .   1.0   .

           stop_

        save_

    """

    print(result.stdout)
    result = isolate_frame(result.stdout, "nef_rdc_restraint_list_rdcs")

    assert_lines_match(EXPECTED, result)


def test_short_complete_csv():
    sequence_path = path_in_test_data(__file__, "3a_ab.neff")
    csv_path = path_in_test_data(__file__, "short_complete.csv")

    nef_sequence = open(sequence_path, "r").read()

    args = [csv_path]
    result = run_and_report(app, args, input=nef_sequence)

    EXPECTED = """\
        save_nef_rdc_restraint_list_rdcs
           _nef_rdc_restraint_list.sf_category           nef_rdc_restraint_list
           _nef_rdc_restraint_list.sf_framecode          nef_rdc_restraint_list_rdcs
           _nef_rdc_restraint_list.restraint_origin      .
           _nef_rdc_restraint_list.tensor_magnitude      .
           _nef_rdc_restraint_list.tensor_rhombicity     .
           _nef_rdc_restraint_list.tensor_chain_code     .
           _nef_rdc_restraint_list.tensor_sequence_code  .
           _nef_rdc_restraint_list.tensor_residue_name   .

           loop_
              _nef_rdc_restraint.index
              _nef_rdc_restraint.restraint_id
              _nef_rdc_restraint.restraint_combination_id
              _nef_rdc_restraint.chain_code_1
              _nef_rdc_restraint.sequence_code_1
              _nef_rdc_restraint.residue_name_1
              _nef_rdc_restraint.atom_name_1
              _nef_rdc_restraint.chain_code_2
              _nef_rdc_restraint.sequence_code_2
              _nef_rdc_restraint.residue_name_2
              _nef_rdc_restraint.atom_name_2
              _nef_rdc_restraint.weight
              _nef_rdc_restraint.target_value
              _nef_rdc_restraint.target_value_uncertainty
              _nef_rdc_restraint.lower_linear_limit
              _nef_rdc_restraint.lower_limit
              _nef_rdc_restraint.upper_limit
              _nef_rdc_restraint.upper_linear_limit
              _nef_rdc_restraint.scale
              _nef_rdc_restraint.distance_dependent

             0   0   .   AAAA   11   .   HA     AAAA   11   .   HN   1.0   1.3   1.0   .   .   .   .   1.0   .
             1   1   .   AAAA   11   .   HB     AAAA   11   .   HN   1.0   4.6   2.0   .   .   .   .   1.0   .
             2   2   .   AAAA   12   .   HG3#   AAAA   12   .   HN   1.0   2.4   3.0   .   .   .   .   1.0   .
             3   3   .   AAAA   13   .   HA     AAAA   13   .   HN   1.0   6.7   4.0   .   .   .   .   1.0   .

           stop_

        save_

    """

    print(result.stdout)
    result = isolate_frame(result.stdout, "nef_rdc_restraint_list_rdcs")

    assert_lines_match(EXPECTED, result)
