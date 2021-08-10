import os
from datetime import date
import sys

from seckerwiki.util import bcolors


def journal(cfg, args):
    if args.encrypt:
        encrypt_journal(cfg, args)
    elif args.decrypt:
        decrypt_journal(cfg, args)
    else:
        today = date.today().isoformat()
        filename = 'entry-{0}.md'.format(today)
        text = '# Journal Entry -  {0}\n\n - '.format(today)

        path = os.path.join(cfg['wiki-root'], cfg['journal-path'], filename)

        with open(path, 'a') as f:
            f.write(text)
            print("Generated Journal Entry: ", path)

def encrypt_journal(cfg, args):
    journal_dir = os.path.join(cfg['wiki-root'], cfg['journal-path'])

    # check if journal path exists
    if not os.path.isdir(journal_dir):
        print("Journal directory not found: {0}".format(journal_dir))
        return

    print("Encrypting Journal Entries...")
    for root, dirs, files in os.walk(journal_dir):
        for file in files:
            # only encrypt markdown files
            if not file.endswith(".md"):
                print("Skipping: {0}{1}{2}".format(bcolors.OKBLUE, file, bcolors.ENDC))
                continue

            print("Encrypting: {0}{1}{2}".format(bcolors.OKGREEN, file, bcolors.ENDC))
            os.system(
                "gpg -c --armor --batch --passphrase {0} {1}".format(cfg['journal-password'], os.path.join(root, file)))
            # delete the markdown file
            os.remove(os.path.join(root, file))


def decrypt_journal(cfg, args):
    journal_dir = os.path.join(cfg['wiki-root'], cfg['journal-path'])

    # check if journal path exists
    if not os.path.isdir(journal_dir):
        print("Journal directory not found: {0}".format(journal_dir))
        return

    path = os.path.abspath(args.decrypt)

    print("Decrypting Journal Entry: {0}{1}{2}".format(bcolors.OKGREEN, path, bcolors.ENDC), file=sys.stderr)
    os.system("gpg -d --armor --batch --passphrase {0} {1}".format(cfg['journal-password'], path))
