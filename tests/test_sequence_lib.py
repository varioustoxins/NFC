from textwrap import dedent

import pytest

from lib.sequence_lib import translate_1_to_3, sequence_3let_to_sequence_residues, BadResidue, frame_to_chains, count_residues
from lib.structures import SequenceResidue
from pynmrstar import Saveframe

ABC_SEQUENCE_1LET = 'acdefghiklmnpqrstvwy'
ABC_SEQUENCE_3LET = (
        'ALA',
        'CYS',
        'ASP',
        'GLU',
        'PHE',
        'GLY',
        'HIS',
        'ILE',
        'LYS',
        'LEU',
        'MET',
        'ASN',
        'PRO',
        'GLN',
        'ARG',
        'SER',
        'THR',
        'VAL',
        'TRP',
        'TYR'
)

ABC_SEQUENCE_RESIDUES = [SequenceResidue('A', i+1, residue) for (i, residue) in enumerate(ABC_SEQUENCE_3LET)]


def test_1let_3let():

    assert len(ABC_SEQUENCE_1LET) == 20
    assert len(ABC_SEQUENCE_3LET) == 20

    assert list(ABC_SEQUENCE_3LET) == translate_1_to_3(ABC_SEQUENCE_1LET)


def test_bad_1let_3let():
    BAD_SEQUENCE = 'acdefghiklmonpqrstvwy'

    msgs = '''\
              unknown residue O
              at residue 12
              sequence: acdefghiklmonpqrstvwy
              ^
              '''

    msgs = dedent(msgs)
    msgs = msgs.split('\n')

    with pytest.raises(BadResidue) as exc_info:
        translate_1_to_3(BAD_SEQUENCE)

    for msg in msgs:
        assert msg in exc_info.value.args[0]


def test_3let_sequence_residue():

    sequence_residues = sequence_3let_to_sequence_residues(ABC_SEQUENCE_3LET)

    assert sequence_residues == ABC_SEQUENCE_RESIDUES


def test_3let_sequence_residue_diff_chain():
    sequence_residues = sequence_3let_to_sequence_residues(ABC_SEQUENCE_3LET, chain_code='B')

    expected = [SequenceResidue('B', residue.sequence_code, residue.residue_name) for residue in ABC_SEQUENCE_RESIDUES]

    assert sequence_residues == expected


def test_3let_sequence_residue_offset():
    sequence_residues = sequence_3let_to_sequence_residues(ABC_SEQUENCE_3LET, offset=-10)

    expected = [SequenceResidue(residue.chain_code, residue.sequence_code - 10, residue.residue_name) for residue in ABC_SEQUENCE_RESIDUES]

    assert sequence_residues == expected


TEST_DATA_MULTI_CHAIN = """
    save_nef_molecular_system
       _nef_molecular_system.sf_category   nef_molecular_system
       _nef_molecular_system.sf_framecode  nef_molecular_system

       loop_
          _nef_sequence.index
          _nef_sequence.chain_code
          _nef_sequence.sequence_code
          _nef_sequence.residue_name
          _nef_sequence.linking
          _nef_sequence.residue_variant
          _nef_sequence.cis_peptide
          _nef_sequence.ccpn_comment
          _nef_sequence.ccpn_chain_role
          _nef_sequence.ccpn_compound_name
          _nef_sequence.ccpn_chain_comment

         1    A   3    HIS   .   .   .   .   .   Sec5   .    
         2    A   4    MET   .   .   .   .   .   Sec5   .    
         3    B   5    ARG   .   .   .   .   .   Sec5   .    
         4    B   6    GLN   .   .   .   .   .   Sec5   .    
         5    C   7    PRO   .   .   .   .   .   Sec5   .       

       stop_

    save_

    """

def test_list_chains():

    test_frame = Saveframe.from_string(TEST_DATA_MULTI_CHAIN)
    chains = frame_to_chains(test_frame)

    assert chains == list(['A', 'B', 'C'])


def test_list_chains_no_chains():
    TEST_DATA = """
    save_nef_molecular_system
       _nef_molecular_system.sf_category   nef_molecular_system
       _nef_molecular_system.sf_framecode  nef_molecular_system

       loop_
          _nef_sequence.index
          _nef_sequence.chain_code
          _nef_sequence.sequence_code
          _nef_sequence.residue_name
          _nef_sequence.linking
          _nef_sequence.residue_variant
          _nef_sequence.cis_peptide
          _nef_sequence.ccpn_comment
          _nef_sequence.ccpn_chain_role
          _nef_sequence.ccpn_compound_name
          _nef_sequence.ccpn_chain_comment

         1    .   3    HIS   .   .   .   .   .   Sec5   .    

       stop_

    save_

    """
    test_frame = Saveframe.from_string(TEST_DATA)
    chains = frame_to_chains(test_frame)

    assert chains == list([])


def test_count_chains():
    test_frame = Saveframe.from_string(TEST_DATA_MULTI_CHAIN)

    result = {}
    for chain in 'ABC':
        result[chain] = count_residues(test_frame, chain)

    EXPECTED = {'A': {'HIS': 1, 'MET': 1}, 'B': {'ARG': 1, 'GLN': 1}, 'C': {'PRO': 1}}
    assert result == EXPECTED

if __name__ == '__main__':
    pytest.main([f'{__file__}', '-vv'])