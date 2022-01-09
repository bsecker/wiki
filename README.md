# Seckerwiki Scripts

This package is a CLI that helps me manage my markdown-based [Foam](https://foambubble.github.io/) workspace, or my "Personal Wiki".
I store everything in my wiki, from journal entries to uni notes.

## Installation

Version `1.x` had requirements for extra dependencies to get the lecture-to-markdown converter working properly. Since I no longer go to uni, I don't need those scripts anymore, so the installation is as simple as:

```
pip3 install seckerwiki
```

Once installed, run this command to generate the config files:

```
wiki setup
```

## Commands

### Setup

This command does a couple of things:

- Creates a `config.yml` file in `~/.config/seckerwiki`, which is used to configure some things in the repo.
- Creates a `credentials` file in `~/.config/seckerwiki/`, which stores secrets.

Edit the credentials file to add a secret passsword used for decrypting your Journal (see below).

### log 

Alias for git log, with some pretty graph options.

### status

Runs `git status`. Basically just a convenience function, so you don't have to `cd` into a wiki dir.

### commit 

does a git commit, generating a commit message. If there are a number of staged files, the commit header shows the top level folders instead.

Args:

- `-y`: skip verification and commit
- `-a`: also do `git add --all`

### sync

perform a `git pull` (rebase) then `git push`

### journal

I use my wiki to store encrypted journal entries.

Run `wiki journal` to generate a new empty journal entry in the journal folder specified in the settings. `wiki journal --encrypt` replaces all the `.md` files with `.md.asc` files, encrypting the files with a symmetric key specified in the settings. `wiki journal --decrypt [filename]` decrypts a file in the encrypted journal directory and prints it to stdout.

### toc

Generates a table of contents for other files/subfolders the markdown file is.

Add the following tags to the "contents/readme" page in each subfolder:

```
<!--BEGIN_TOC-->
<!--END_TOC-->
```

The script will replace the content between these two tags with the contents. For example:

```
<!--BEGIN_TOC-->
Pages:
- [hardware](./hardware.md)
- [iot-development](./iot-development.md)
- [iot-platforms](./iot-platforms.md)
- [platformio-esp32-notes](./platformio-esp32-notes.md)
- [rtoses](./rtoses.md)

<!--END_TOC-->
```

This is used primarily so [Foam](https://foambubble.github.io/foam/features/graph-visualisation.html) can build a graph that collects pages within a folder together by a node.

### stats

Prints some cool stats about the wiki:

- `commits made` - number of git commits since repo was created
- `Number of notes` - number of markdown files in repo
- `total lines` - non-empty lines in `.md` files
- `largest files` - paths to the top 3 longest `.md` files


## Developing

I use [poetry](https://python-poetry.org/) for building/publishing the package. Read their docs.