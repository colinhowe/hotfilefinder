import argparse
import subprocess

DESCRIPTION = """Process a git repo's history and list out all the files in
order of their hotness.

Hotness is the number of times that the file has been modified."""

def _get_git_log(path):
    """
    Gets the git log at the given path.
    """
    out = []
    p = subprocess.Popen(['git', 'log'], stdout=subprocess.PIPE, cwd=path)
    for line in p.stdout:
        out.append(line)
    p.wait()
    return out

def calculate_hotness(path):
    """
    Calculates the hotness of the git repo at the given path.

    The return value will be a dictionary of paths to hotness (number of times
    modified).
    """
    print _get_git_log(path)
    return {'./blah': 1}

def _process_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('path',
                       help='path to the git repo')
    return parser.parse_args()

if __name__ == '__main__':
    args = _process_args()

    hotness = calculate_hotness(args.path)
    hotness = sorted(hotness.iteritems(), key=lambda item: item[1])
    print hotness

