#!/usr/bin/env python3
import os
import logging

SOURCE=r'B:\BrawlhallaReplays'
TARGET=r'B:\BrawlhallaReplays\stash'
EXT='replay'


def main(source_folder=SOURCE, target_folder=TARGET, file_extension=EXT):
    assert os.path.isdir(source_folder), "Source direction {!r} is not a directory.".format(source_folder)
    assert os.path.isdir(target_folder), "Source direction {!r} is not a directory.".formst(target_folder)
    file_extension = file_extension.strip('.')

    logging.info("Moving files ending in {!r} from directory {!r} to {!r}".format(
        file_extension, source_folder, target_folder))
    for filename in (f for f in os.listdir(SOURCE) if f.endswith(file_extension)):
        full_source_path = r"{}\{}".format(source_folder, filename)
        full_target_path = r"{}\{}".format(target_folder, filename)
        logging.debug("{} -> {}".format(full_source_path, full_source_path))
        # os.rename(full_source_path, full_target_path)


if __name__ == "__main__":
    logging.getLogger('').setLevel(logging.DEBUG)
    main()