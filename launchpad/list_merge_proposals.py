#!/usr/bin/env python3
"""
Find merge requests in a specific state.

Copyright 2018 Canonical Ltd.
Joshua Powers <josh.powers@canonical.com>
"""
import argparse
import getpass
import os

from launchpadlib.launchpad import Launchpad


def main(project, state):
    """Get versions and print"""
    cachedir = os.path.join('/home', getpass.getuser(), '.launchpadlib/cache/')
    launchpad = Launchpad.login_anonymously(
        'ubuntu-server merge proposal lookup', 'production',
        cachedir, version='devel'
    )

    if project.startswith('lp:'):
        branch = launchpad.branches.getByUrl(url=project)
    else:
        branch = launchpad.git_repositories.getByPath(
            path=project.replace('lp:', '')
        )

    if not branch:
        print('No branch named %s found' % project)
        return

    for merge in branch.landing_candidates:
        if state:
            if merge.queue_status in state:
                print('%s' % merge)
        else:
            print('%s' % merge)

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('project', help='project name')
    PARSER.add_argument('--state',
                        help='Work in progress, Needs review, Approved, '\
                             'Rejected, or Merged')

    ARGS = PARSER.parse_args()
    main(ARGS.project, ARGS.state)
