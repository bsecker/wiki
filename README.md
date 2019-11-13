# Wiki/Productivity Scripts

This repo provides a set of scripts used to improve the functionality of markdown-based gitlab wikis.
It also has some handy scripts to help my uni workflow.

Gitlab repositories have their own wiki, which is contained in a separate git repo.

## Install/Setup

create a new config file:

```bash
cp config-example.yml config.yml
```

Edit the config as required.

TODO put some docs here

## Scripts

### Nested Sidebar Generator

Sidebars in gitlab are annoying as hell. They don't support nested directories, and a sidebar for a large wiki gets super unwieldy.  

this script generates a `_Sidebar.md` file which can be added to the root wiki directory for proper nested sidebars.

![](images/sidebars.png)

```
usage: sidebar_generator.py [-h] [--exclude EXCLUDE [EXCLUDE ...]]
                            [--max-depth MAX_DEPTH] [--hide-files] [--save]
                            [--wiki WIKI]

optional arguments:
  -h, --help            show this help message and exit
  --exclude EXCLUDE [EXCLUDE ...]
                        list of directories names to exclude. Includes all
                        subdirectories. Defaults to config file exclusions
  --max-depth MAX_DEPTH
                        maximum depth to build tree
  --hide-files          Only build the sidebar using directories, hiding files
  --save                save to _Sidebar.md in wiki directory, instead of
                        outputting to stdout
  --wiki WIKI           wiki root directory

```

note that the `--exclude` defaulting to the config file isn't yet implemented - it defaults to none.

### Subdirectory Contents Page Generator

description of why I made this

### Lecture Slides from URL

description of why I made this

### script title
