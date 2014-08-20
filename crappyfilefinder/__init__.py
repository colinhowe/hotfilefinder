import argparse
import collections
import subprocess

DESCRIPTION = """Process a git repo's history and list out all the files in
order of their hotness.

Hotness is the number of lines that have been modified. This count excludes
changes due to creation/deletion of entire files. E.g. if a file is created
with 10 lines then 5 more are added, the hotness will be 5."""

def calculate_hotness(path, since=None, until=None):
    """
    Calculates the hotness of the git repo at the given (git) path.

    since and until are dates that will be passed through to git log without
    change.

    The return value will be a dictionary of paths to hotness (number of times
    modified).
    """
    log = _get_git_log(path, since=since, until=until)
    commits = _group_into_commits(log)
    # Process commits in reverse order so that deleted files are ignored.
    commits = reversed(list(commits))
    changes = [_parse_commit_change_size(commit) for commit in commits]
    totals = _combine_changes(changes)
    return totals

def _get_git_log(path, since, until):
    """
    Gets the git log at the given path.
    """
    args = ['git', 'log', '--summary', '--numstat', '--format=format:']
    if since:
        args.append('--since=%s' % since)
    if until:
        args.append('--until=%s' % until)
    if path:
        args.append(path)
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    out = [line.rstrip() for line in p.stdout]
    p.wait()
    if p.returncode != 0:
        raise Exception('Git failed')
    return out

def _group_into_commits(log):
    commit = None
    for line in log:
        if not line:
            if commit:
                yield commit
            commit = []
        else:
            commit.append(line)
    if commit:
        yield commit

def _parse_commit_change_size(commit):
    """
    Parses git's change stat format:
        5 10 blah.py
    Indicates 5 new lines, 10 removed lines in blah.py

    This will exclude any changes due to creation.

    If a file has been deleted it will be returned with a value of -1.
    """
    result = {}
    for line in commit:
        if line.startswith(' delete'):
            path = line.split(' ', 4)[-1]
            result[path] = -1
        elif line.startswith(' create'):
            path = line.split(' ', 4)[-1]
            if path in result:
                del result[path]
        elif line.startswith(' mode'):
            continue
        else:
            try:
                incr, decr, path = line.split('\t')
            except ValueError:
                print '\n'.join(commit)
                raise
            # binary files are specified as - - instead of number differences
            if incr == '-' or decr == '-':
                continue
            result[path] = int(incr) + int(decr)
    return result

def _combine_changes(commits):
    result = collections.defaultdict(int)
    for commit in commits:
        for path, value in commit.iteritems():
            if value == -1:
                if path in result:
                    del result[path]
            else:
                result[path] += value
    return result

def _process_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-path',
        help='path to the git repo')
    parser.add_argument('--since',
        help='date to limit commits from')
    parser.add_argument('--until',
        help='date to limit commits until')
    parser.add_argument('-n', type=int, default=20,
        help='number of results to output. Specifying 0 will output all.'
        + ' Default 20')
    return parser.parse_args()

if __name__ == '__main__':
    args = _process_args()

    hotness = calculate_hotness(
        args.path or '',
        since=args.since, until=args.until)
    hotness = sorted(hotness.iteritems(), reverse=True, key=lambda item: item[1])
    if args.n:
        hotness = hotness[:args.n]
    for path, value in hotness:
        print path, '\t', value
