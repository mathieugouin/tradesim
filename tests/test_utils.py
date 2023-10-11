"""Testing utilities library."""

# To make print working for Python2/3
from __future__ import print_function

import os
import shutil


def empty_folder_content(folder):
    """Remove all files and subfolder from a folder."""
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def list_folder_content(folder):
    """List all files recursively from a folder."""
    matches = []
    #         dirnames unused
    for root, _,       filenames in os.walk(folder):
        for filename in filenames:
            matches.append(os.path.join(root, filename))
    return matches


def empty_folder_and_confirm(folder):
    empty_folder_content(folder)
    assert len(list_folder_content(folder)) == 0
