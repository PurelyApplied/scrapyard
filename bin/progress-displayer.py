#!/usr/bin/env python3
import logging
import re
import argparse
from enum import Enum

from termcolor import colored

START_REGEX = re.compile("Starting test (.*)$")
COMPLETE_REGEX = re.compile("Completed test (.*) with result: (.*)$")

# Start character
top_corner_char = u'\u2553'
# Continuation character
vertical_char = u'\u2551'
# End character
bottom_corner_char = u'\u2559'


class Statuses(str, Enum):
    starting = "Starting"
    success = "SUCCESS"
    failed = "FAILURE"
    skipped = "SKIPPED"

    @classmethod
    def is_end_status(cls, status, include_skipped=True):
        return status in (cls.success, cls.failed) or (include_skipped and status == cls.skipped)

    @classmethod
    def to_color(cls, status):
        if status == cls.success:
            return "green"
        if status == cls.failed:
            return "red"
        if status == cls.skipped:
            return "yellow"
        return None

    @classmethod
    def to_start_or_stop_char(cls, status):
        return bottom_corner_char if cls.is_end_status(status) else top_corner_char


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
        return (f"ProgressEntry({self.line_number}, '{self.line_string[:20]} ...', *,"
                f" status={self.status}, test_name={self.test_name})")

    def __gt__(self, other):
        return self.line_number > other.line_number


class ProgressReport:
    def __init__(self, *entries: ProgressEntry):
        self.line_to_entry = {}
        self.test_to_entry_pair_dict = {}

        for e in entries:
            self.add_entry(e)

    def add_entry(self, entry):
        self.line_to_entry[entry.line_number] = entry

        pair_dict = self.test_to_entry_pair_dict.get(entry.test_name, {})
        pair_dict[entry.start_or_end] = entry
        self.test_to_entry_pair_dict[entry.test_name] = pair_dict

    def get_end_entry_for_test(self, test_key):
        return self.test_to_entry_pair_dict[test_key].get('end')

    def get_end_status_for_test(self, test_key):
        entry = self.get_end_entry_for_test(test_key)
        # If a test fails and does not end, the above may return None.  Return None status in this case.
        return entry.status if entry else None

    def get_maximum_concurrent_tests(self, include_skipped_tests=True):
        # Skipped tests still get entries for Starting... immediately followed by SKIPPED.
        maximum_concurrent = 0
        current_concurrent = 0
        for index, entry in sorted(self.line_to_entry.items()):
            if entry.status is Statuses.skipped and not include_skipped_tests:
                continue

            if entry.status is Statuses.starting:
                current_concurrent += 1
            elif entry.status in (Statuses.success, Statuses.failed, Statuses.skipped):
                current_concurrent -= 1
            else:
                raise RuntimeError(f"Got unexpected status: '{entry.status}' in entry: {entry}")
            maximum_concurrent = max((maximum_concurrent, current_concurrent))
        return maximum_concurrent


def character_and_color(l, this_entry, report):
    if l is None:
        return " "
    end_entry = report.get_end_entry_for_test(l.test_name)
    color = Statuses.to_color(end_entry.status) if end_entry else None
    character = Statuses.to_start_or_stop_char(this_entry.status) if l.test_name == this_entry.test_name else vertical_char
    return colored(character, color)


def to_next_row(l):
    return None if l is None or Statuses.is_end_status(l.status) else l


def new_main(filename):
    raw_lines = open(filename).readlines()
    progress_entries = [ProgressEntry(i, l) for i, l in enumerate(raw_lines)]
    progress_report = ProgressReport(*progress_entries)
    maximum_concurrent = progress_report.get_maximum_concurrent_tests(True)
    sorted_entry_list = sorted(progress_report.line_to_entry.items())
    tracks = []
    eliminate_previous = None
    for index, entry in sorted_entry_list:
        # The lane always points at the end event for the corresponding test, to get colors right.
        # If this entry equals that "end" entry, then we eliminate with a hook.
        this_lane = tracks[-1].copy() if tracks else [None] * (maximum_concurrent + 1)
        if eliminate_previous:
            this_lane[this_lane.index(eliminate_previous)] = None
            eliminate_previous = None

        if entry.status is Statuses.starting:
            first_open = this_lane.index(None)
            this_lane[first_open] = progress_report.get_end_entry_for_test(entry.test_name)
        elif Statuses.is_end_status(entry.status):
            # Mark this for next loop
            eliminate_previous = entry
        else:
            raise RuntimeError("Woah")

        tracks.append(this_lane)

    for lane, (index, this_entry) in zip(tracks, sorted_entry_list):
        lane_chars = [character_and_color(l, this_entry, progress_report) for l in lane]
        print(
            " ".join(lane_chars) + "   " + colored(this_entry.line_string.strip(), Statuses.to_color(this_entry.status)))
    return

    print(maximum_concurrent)
    return maximum_concurrent
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
    # logging.getLogger().setLevel(logging.DEBUG)
    new_main(args.progfile)
