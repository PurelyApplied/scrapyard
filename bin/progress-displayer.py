#!/usr/bin/env python3
import logging
import re
import argparse
from enum import Enum

from termcolor import colored

START_REGEX = re.compile("Starting test (.*)$")
COMPLETE_REGEX = re.compile("Completed test (.*) with result: (.*)$")

top_corner_char = u'\u2553'
vertical_char = u'\u2551'
bottom_corner_char = u'\u2559'


class Statuses(str, Enum):
    starting = "Starting"
    success = "SUCCESS"
    skipped = "SKIPPED"


class ProgressEntry:
    def __init__(self, line_number=None, line_string=None):
        self.line_number = line_number
        self.line_string = line_string

        self.start_or_end = None
        self.test_name = None
        self.status = None
        self._parse_line()

    def _parse_line(self):
        if START_REGEX.search(self.line_string):
            self.test_name = START_REGEX.search(self.line_string).group(1)
            self.status = Statuses.starting
            self.start_or_end = "start"
        elif COMPLETE_REGEX.search(self.line_string):
            self.test_name = COMPLETE_REGEX.search(self.line_string).group(1)
            self.status = COMPLETE_REGEX.search(self.line_string).group(2)
            self.start_or_end = "end"
        else:
            raise RuntimeError("Unexpected line format in line: " + self.line_string)

    def __repr__(self):
        return f"ProgressEntry({self.line_number}, {self.line_string})"


class ProgressReport:
    def __init__(self, *entries: ProgressEntry):
        # d[line_num] = entry
        self.line_to_entry = {}
        # d['test']['start'] = entry
        self.test_to_entry_pair_dict = {}

        for e in entries:
            self.add_entry(e)

    def add_entry(self, e):
        self.line_to_entry[e.line_number] = e

        pair_dict = self.test_to_entry_pair_dict.get(e.test_name, {})
        pair_dict[e.start_or_end] = e
        self.test_to_entry_pair_dict[e.test_name] = pair_dict


def new_main(filename):
    raw_lines = open(filename).readlines()
    progress_entries = [ProgressEntry(i, l) for i, l in enumerate(raw_lines)]
    progress_report = ProgressReport(*progress_entries)
    print(progress_entries)

def main(filename):
    lines = open(filename).readlines()
    test_status = {}

    occupied_tracks = {}  # test -> position
    tracks = [{}]  # list of dicts [ position -> char ]

    # Do a pass to see how much preamble I'm going to need
    for i, l in enumerate(lines):
        l = l.strip()
        logging.debug("Previous tracks: ", tracks[-1])
        current_tracks = {k: vertical_char for k, v in tracks[-1].items() if v != bottom_corner_char}
        for k, v in tracks[-1].items():
            if v == bottom_corner_char:
                occupied_tracks = {k2: v2 for k2, v2 in occupied_tracks.items() if v2 != k}
        logging.debug("Tracks to use this iteration: ", current_tracks)

        if START_REGEX.search(l):
            test_name = START_REGEX.search(l).group(1)
            if test_name in test_status:
                raise RuntimeError("Bad line with test_name in test_status: " + l)
            test_status[test_name] = None
            position = get_available_position(occupied_tracks)
            occupied_tracks[test_name] = position
            current_tracks[position] = top_corner_char
        elif COMPLETE_REGEX.search(l):
            test_name = COMPLETE_REGEX.search(l).group(1)
            result = COMPLETE_REGEX.search(l).group(2)
            if test_name not in test_status:
                raise RuntimeError("Bad line with test_name not in test_status: " + l)
            test_status[test_name] = result
            current_tracks[occupied_tracks[test_name]] = bottom_corner_char
        else:
            raise RuntimeError("Bad line: " + l)

        logging.debug("Updated current tracks, about to append: ", current_tracks)
        logging.debug("\n")
        tracks.append(current_tracks)

    # Remove initial empty.
    tracks.pop(0)

    assert len(lines) == len(tracks)

    concurrent_tracks = max([v for d in tracks for v in d.keys()]) + 1

    for l, t in zip(lines, tracks):
        this_line = get_front_pad(t, concurrent_tracks) + l.strip()
        if "Starting" in this_line:
            print(this_line)
        elif "Completed" in this_line:
            if "SUCCESS" in this_line:
                cprint(this_line, "green")
            elif "SKIPPED" in this_line:
                cprint(this_line, "yellow")
            else:
                cprint(this_line, "red")
        else:
            cprint(this_line, "yellow")


def get_front_pad(d: dict, l: int, spacing=" "):
    tracks = {i: " " for i in range(l)}
    tracks.update(d)
    return spacing + spacing.join((tracks[i] for i in range(l))) + spacing


def cprint(l, c):
    print(colored(l, c))


def get_available_position(positions: dict):
    values = list(positions.values())
    size = len(values)
    possible_values = set(range(size + 1))
    ret = min(possible_values.difference(values))
    logging.debug("values: ", values)
    logging.debug("size: ", size)
    logging.debug("possible: ", possible_values)
    logging.debug("return: ", ret)
    return ret


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('progfile', type=str, help='Progress file from a DUnit test run')
    args = parser.parse_args()
    new_main(args.progfile)
