from argparse import Namespace
from pathlib import Path
from typing import List, Iterable

import typer

from lib.sequence_lib import chain_code_iter
from lib.structures import ShiftList
from lib.typer_utils import get_args
from lib.util import exit_error, process_stream_and_add_frames
from transcoders.nmrpipe.nmrpipe_lib import read_db_file_records, gdb_to_3let_sequence, read_shift_file
from transcoders.nmrpipe import import_app
from lib.util import cached_file_stream
from lib.shift_lib import shifts_to_nef_frame

app = typer.Typer()

# noinspection PyUnusedLocal
@import_app.command()
def shifts(
    chain_codes: str = typer.Option('A', '--chains', help='chain codes as a list of names spearated by dots',
                                   metavar='<CHAIN-CODES>'),
    entry_name: str = typer.Option('nmrpipe', help='a name for the entry'),
    pipe: Path = typer.Option(None, metavar='|PIPE|',
                              help='pipe to read NEF data from, for testing [overrides stdin !use stdin instead!]'),
    file_names: List[Path] = typer.Argument(..., help='input files of type nmrpipe.tab', metavar='<TAB-FILE>')
):
    """convert nmrpipe shift file <nmrpipe>.tab files to NEF"""
    try:
        args = get_args()

        process_shifts(args)
    except Exception as e:
        exit_error(f"reading sequence failed because {e}", e)


def process_shifts(args: Namespace):
    nmrpipe_frames = []

    for file_name, chain_code in zip(args.file_names, chain_code_iter(args.chain_codes)):
        # cached_file_stream
        with cached_file_stream(file_name) as lines:

            nmrpipe_shifts = read_shifts(lines, chain_code=chain_code)

            frame = shifts_to_nef_frame(nmrpipe_shifts, args.entry_name)

            nmrpipe_frames.append(frame)

    entry = process_stream_and_add_frames(nmrpipe_frames, args)

    print(entry)


def read_shifts(shift_lines: Iterable[str], chain_code: str = 'A', sequence_file_name: str = 'unknown') -> ShiftList:

    gdb_file = read_db_file_records(shift_lines, sequence_file_name)

    return read_shift_file(gdb_file, chain_code)


if __name__ == '__main__':

    typer.run(sequence)