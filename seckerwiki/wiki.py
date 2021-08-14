#!/usr/bin/env python3
import argparse
import os
import sys
import yaml

from commands.lecture import lecture
from commands.git import commit, log, sync
from commands.receipt import receipt
from commands.journal import journal
from commands.setup import setup

from util import get_cfg_file

def main():

  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers()

  # Add all the subparsers 
  lecture_parser = subparsers.add_parser('lecture', help='create new lecture slides')
  lecture_parser.add_argument('-b', '--blank', action='store_true', help='Create blank lecture slides.')
  lecture_parser.set_defaults(func=lecture)

  setup_parser = subparsers.add_parser('setup', help='setup wiki CLI')
  setup_parser.set_defaults(func=setup)

  log_parser = subparsers.add_parser('log', help='show git log')
  log_parser.set_defaults(func=log)

  commit_parser = subparsers.add_parser('commit', help='commit wiki')
  commit_parser.add_argument('-y', action='store_true', help='Don\'t ask for confirmation before committing')
  commit_parser.set_defaults(func=commit)

  sync_parser = subparsers.add_parser('sync', help='sync with remote repo')
  sync_parser.set_defaults(func=sync)

  journal_parser = subparsers.add_parser('journal', help='make journal entry')
  journal_parser.add_argument('-e', '--encrypt', action='store_true', help='encrypt all unencrypted journal entries')
  journal_parser.add_argument('-d', '--decrypt', help='decrypt journal entry')
  journal_parser.set_defaults(func=journal)

  args = parser.parse_args()

  # print help and exit if no arguments supplied
  if not hasattr(args, 'func'):
    parser.print_help()
    exit(0)

  # run setup script without config
  if args.func is setup:
    setup()
    sys.exit()

  # Load custom config if defined in env var
  cfg = None
  try:
    cfg_file = os.environ['WIKI_CONFIG'] if 'WIKI_CONFIG' in os.environ else os.path.expanduser('wiki.yml')
    with open(os.path.abspath(cfg_file), 'r') as f:
      cfg = yaml.safe_load(f)
  except FileNotFoundError:
    print("Config file not found at ~/.personal.yml or defined in $WIKI_CONFIG. Have you ran `wiki setup`?")
    sys.exit(1)

  # Run the subcommand
  args.func(cfg, args)


if __name__ == "__main__":
  main()