# Seckerwiki Scripts

This package contains various scripts for managing my markdown-based wiki monorepo.  
I store everything from lecture notes to journal entries in my wiki.
The main command, `wiki`, has functions for downloading slides, setting labels, cross referencing docs and more! see [usage](#usage)

## Installation

Dependencies: 

- _poppler_ if using a mac (`brew install poppler`)
- _unoconv_ for converting pptx to pdf ([link](https://github.com/unoconv/unoconv))
- _gpg_ for journal encryption/decryption

Install the package & pip dependencies

```
pip install --user seckerwiki
```

(mac only?) Add the scripts path to your `$PATH` variable, as described in the pip install logs

```shell script
export PATH=$PATH:/path/to/wiki/scripts
```

Set up configuration file

```
wiki setup
```

Configure wiki scripts

```
vim ~/.personal.yml
```

See [config](#config) for configuration file details.

## Wiki structure

I stick to the following wiki structure. Currently, the lecture generation scripts assume this structure.

``` 
wiki_root/
    Personal/
        Personal-Management/
            Journal/
    Uni/
        General/
        Tri-1/
            COURSE_CODE/
                Lectures/
                    images/
                    lecture-01-name.md
                Assignments/
        Tri-2/
        Full-Year/
    Scripts/
```

## Usage

This section shows off a brief explanation of each command in the wiki script.

### Lecture

Initiates an interactive script for downloading pdf or pptx lecture slides, converts them into individual images, and places 
the images onto a markdown file.
Markdown is a great way to store lecture notes because the plain text format is _simple and reliable_.
The images have the content and extra annotations can be written under each slide.
A version controlled git repository of lecture notes will be around forever.

### Setup

Sets up the wiki CLI configuration file with some default values. See [config](#config) for details.

### log 

Alias for git log, with some pretty graph options.

### open

runs `[editor] /path/to/wiki`, where `editor` is the editor command, for example `code` (vscode) or `vim`

### commit 

does a git commit, generating a commit message. If there are a number of staged files, the commit header shows the top level folders instead.

### todo

grep for TODOs in the wiki.

### sync

perform a `git pull` then `git push`

### tags

To horizontally group wiki pages in different directories, I implemented a simple _document tagging_ system.
In the top line of each file, a comment can be added to add tags in the following format:

```
<!-- tags: tag1, tag2, tag3 -->
```

Running `wiki tags --union` will show all the tags. Running with one or more arguments will reduce the output to files that have _all_ of the tags supplied (alternatively, add the --union tag to show all files that contain _any_ of the supplied tags).
For example, `wiki tags todo project` will show all files that have BOTH `todo` and `project` tags.

I have a few things planned to improve this:

- Cache the outputs so it doesn't search the wiki tree each time
- better visualisation 
- rewrite the function (bit of a mess atm)

### journal

I use my wiki to store encrypted journal entries.

Run `wiki journal` to generate a new empty journal entry in the journal folder specified in the settings. `wiki journal --encrypt` replaces all the `.md` files with `.md.asc` files, encrypting the files with a symmetric key specified in the settings. `wiki journal --decrypt [path]` decrypts a file and prints it to stdout.

### links

open a list of links in your favourite browser. Great for quickly bringing up most commonly used tabs when you start the computer.

### receipt (WIP)

Save a receipt to the wiki (todo)

### build (WIP)

build the markdown into html/pdf files (todo)

## Config

When running `wiki setup`, it generates the following example config file (added some comments here to explain the options):

```yaml
wiki-root: /home/benjamin/Personal/personal # root directory of the wiki
journal-path: Personal/Personal-Management/Journal # relative path from root to the journal directory
journal-password: password # symmetric key for encypting journal articles
courses: # list of lists of courses separated by semester/trimester
  tri-1:
    - COMP424
    - NWEN438
    - ENGR401
  tri-2:
    - NWEN439
    - SWEN430
    - ENGR441
  full-year:
    - ENGR489
links: # list of links to open when running the `wiki links` command
  - https://trello.com/
  - https://mail.google.com/mail/?shva=1#inbox
  - https://calendar.google.com/calendar/r
  - https://clockify.me/tracker
browser-command: firefox # terminal command to open web browser
editor-command: code # terminal command to open text editor
```

