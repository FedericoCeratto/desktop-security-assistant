#!/usr/bin/env python

"""
.. module:: security-assistant
   :synopsis: Security Assistant

"""

# Released under AGPLv3+ license, see LICENSE

from argparse import ArgumentParser
from glob import glob
from setproctitle import setproctitle
import logging
import os
import subprocess
import yaml

from ui import UI
from utils import get_resource

log = logging.getLogger(__name__)


def setup_logging(debug):
    ch = logging.StreamHandler()
    if debug:
        log.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)


class Check(object):

    def __init__(self, kw):
        keys = ('name', 'desc', 'url', 'risk', 'difficulty',
                'python', 'bash')
        for k in keys:
            setattr(self, k, None)

        self.children = []
        self.depends_on = []
        self.hidden = False
        self.__dict__.update(kw)

    def __repr__(self):
        return repr(self.__dict__)


def find_config_block(configuration, block_name):
    """Recursively find a configuration block"""
    assert isinstance(configuration, list)
    for b in configuration:
        if b.name == block_name:
            return b

    for b in configuration:
        if b.children:
            return find_config_block(b.children, block_name)


def scan_config_blocks(configuration):
    """Recurse through all config blocks, depth-first"""
    assert isinstance(configuration, list)
    for b in configuration:
        yield b
        if b.children:
            for c in scan_config_blocks(b.children):
                yield c


def run_config_block(c):
    """Run commands in a config block, if any, and add the status flag
    """
    if c.python:
        # execute Python code
        log.info("%r: executing Python %r", c.name, c.python)
        try:
            output = eval(c.python)
            c.status = 'active' if output else 'disabled'
            log.info("%r: status %r", c.name, c.status)
        except Exception:
            log.error("%r: error", c.name, exc_info=True)
            c.status = 'error'

    elif c.bash:
        # execute Bash code
        log.info("%r: executing Bash %r", c.name, c.bash)
        try:
            output = subprocess.call(c.bash, shell=True,
                                     executable='/bin/bash')
            c.status = 'active' if output else 'disabled'
            log.info("%r: status %r", c.name, c.status)
        except Exception:
            log.error("%r: error", c.name, exc_info=True)
            c.status = 'error'

    else:
        c.status = 'active'


def scan_and_run_config_blocks(configuration):
    """Recurse through all config blocks, depth-first"""
    assert isinstance(configuration, list)
    for b in configuration:
        run_config_block(b)
        yield b

        # Recurse child confs only on active blocks
        if b.status != 'disabled' and b.children:
            for c in scan_and_run_config_blocks(b.children):
                yield c


def load_configuration_files():
    """Load configuration files"""
    path_glob = get_resource('checks', '*.yaml')
    log.debug("scanning %r", path_glob)
    fnames = sorted(glob(path_glob))
    log.debug("%d config files to be loaded", len(fnames))

    config_blocks = []
    for fn in fnames:
        with open(fn) as f:
            confs = yaml.load(f)
            if not isinstance(confs, list):
                confs = [confs, ]

            for c in confs:
                config_blocks.append(Check(c))

    log.debug("%d config blocks found", len(config_blocks))

    # create config hierarchy
    # extract root blocks
    config_tree = [b for b in config_blocks if not b.depends_on]
    child_blocks = [b for b in config_blocks if b.depends_on]

    while child_blocks:
        for pos, block in enumerate(child_blocks):
            parent = find_config_block(config_tree, block.depends_on)
            if parent is None:
                continue  # hopefully the parent will show up later

            try:
                parent.children.append(block)
            except KeyError:
                parent['children'] = [block, ]

            child_blocks.pop(pos)

    return config_tree


def parse_args():
    ap = ArgumentParser()
    ap.add_argument('-c', '--cli', help='run from command line',
                    action='store_true')
    ap.add_argument('-d', '--debug', help='verbose logging',
                    action='store_true')
    args = ap.parse_args()
    return args


def print_out_checks(checks_to_be_displayed):
    """Print active checks to stdout"""
    for check in checks_to_be_displayed:
        print
        print "Name:        %s" % check.name
        print "Description: %s" % check.desc
        if check.risk:
            print "Risk:        %s" % ('*' * check.risk)

        if check.difficulty:
            print "Difficulty:  %s" % ('*' * check.difficulty)

        if check.url:
            print "URL:         %s" % check.url

    print


def main():
    setproctitle('desktop-security-assistant')
    args = parse_args()
    setup_logging(args.debug)

    conf = load_configuration_files()

    checks_to_be_displayed = []
    for c in scan_and_run_config_blocks(conf):
        if c.status != 'disabled' and not c.hidden:
            checks_to_be_displayed.append(c)

    if args.cli:
        print_out_checks(checks_to_be_displayed)
        return

    ui = UI()
    for c in checks_to_be_displayed:
        ui.add_check_tab(c)

    ui.main()


if __name__ == '__main__':
    main()
