import argparse
import collections
import subprocess

DESCRIPTION = """Process a git repo's history and list out all the files in
order of their hotness.

Hotness is the number of lines that have been modified."""

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
    changes = [_parse_commit_change_size(commit) for commit in commits]
    totals = _combine_changes(changes)
    return totals

def _get_git_log(path, since, until):
    """
    Gets the git log at the given path.
    """
    args = ['git', 'log', '--numstat', '--format=format:']
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
    result = {}
    for line in commit:
        incr, decr, path = line.split('\t')
        result[path] = int(incr) + int(decr)
    return result

def _combine_changes(commits):
    result = collections.defaultdict(int)
    for commit in commits:
        for path, value in commit.iteritems():
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
    return parser.parse_args()

if __name__ == '__main__':
    args = _process_args()

    hotness = calculate_hotness(
        args.path or '',
        since=args.since, until=args.until)
    hotness = sorted(hotness.iteritems(), reverse=True, key=lambda item: item[1])
    for path, value in hotness:
        print path, '\t', value
