"""
Personal text-based launcher that can be used to start my lecture workflow efficiently.

main:
------------------------------
Choose task:
 (1) New lecture
 (2) commit+push wiki
 (3) start atom
"""
import glob
import os
import configparser
import re

tk_enabled = True

try:
    # GUI file handler setup

    from tkinter import Tk
    from tkinter.filedialog import askopenfilename

    root = Tk()
    root.withdraw()
except ImportError as e:
    tk_enabled = False
    print("failed to import tk: ", e)
    pass

# read the configuration file
config = configparser.ConfigParser()
config.read("config.cfg")


def get_latest_lecture_num(course):
    """
    Return the latest lecture number from the filenames in course
    """
    lecture_dir = os.path.join(config['wiki']['wiki_root'], "Uni", course, "Lectures")

    files = [f for f in glob.glob(lecture_dir + "**/*.md", recursive=False)]

    # if no files exist, return 0
    if len(files) < 1:
        print("No recent lectures found.")
        return 1

    last_file = sorted(files)[-1]

    print("Most recent lecture: " + last_file)

    # use regex to match number (get last as most likely to be lecture num)
    last = re.findall(r'\d+', last_file)[-1]

    # suggest the latest lecture num + 1
    suggested = int(last) + 1 if last.isdigit() else "none"

    return suggested


def new_lecture():
    """Use prompt to generate new lecture page"""

    # get link
    print("Enter URL or downloaded PDF path: (enter 'o' to open dialog)")
    pdf_file = input(">")
    if pdf_file == "o" and tk_enabled:
        pdf_file = askopenfilename()  # show an "Open" dialog box and return the path to the selected file

    # get course
    print("Enter course code or ID:")
    print("""
(1) COMP309
(2) SWEN325
(3) SWEN324
(4) ENGR302    
    """)

    chosen_course = input(">")
    if chosen_course == "1" or chosen_course == "COMP309":
        course = "COMP309"
    elif chosen_course == "2" or chosen_course == "SWEN325":
        course = "SWEN325"
    elif chosen_course == "3" or chosen_course == "SWEN324":
        course = "SWEN324"
    elif chosen_course == "4" or chosen_course == "ENGR302":
        course = "ENGR302"
    else:
        return

    # get lecture number
    suggested = get_latest_lecture_num(course)
    print("Enter lecture number (suggested: {0}):".format(suggested))
    num = input(">")

    print("Enter lecture title (or leave blank): ")
    title = input(">")

    # exec launcher script
    title_arg = "--title=\"{0}\"".format(title) if title else ""
    script = "python pdf_lecture_slide_generator.py \"{0}\" {1} {2} {3}".format(pdf_file, course, num, title_arg)
    print(script)
    os.system(script)

    # open file in launcher
    # print("Open in editor? (Y/N)")
    # inp = input(">")
    # if inp == "Y" or inp == "y":
    #     markdown_file = "{0}Uni/{1}/Lectures/lecture_{2}.md".format(config["wiki"]["wiki_root"], course, num)
    #     open_editor(markdown_file)

    return


def commit_wiki():
    """commit the personal wiki with a generic message and push to remote"""
    os.chdir(config["wiki"]["wiki_root"])
    os.system("git diff --quiet && git diff --staged --quiet || git commit -am \"(AUTO) update wiki\"")
    os.system("git pull && git push")


def open_editor(_file=None):
    """Open atom on the wiki folder, or optionally a file"""
    if not _file:
        os.system("atom")
    else:
        os.system("atom {0}".format(_file))


def show_git_status():
    """Run 'git status' in the wiki directory"""
    os.chdir(config["wiki"]["wiki_root"])
    os.system("git status")


def open_chrome_tabs():
    """open the regular chrome tabs. Trello, Google Calendar, mattermost"""
    os.system("google-chrome https://trello.com/b/0GZC5yD9/2019-tri-2")
    os.system("google-chrome https://calendar.google.com/calendar/")
    os.system("google-chrome https://mattermost.ecs.vuw.ac.nz/engr300-2019/channels/project-01")


def new_lecture_empty():
    """Use prompt to generate new lecture page with no pdfs"""

    # get course
    print("Enter course code or ID:")
    print("""
(1) COMP309
(2) SWEN325
(3) SWEN324
(4) ENGR302    
    """)

    chosen_course = input(">")
    if chosen_course == "1" or chosen_course == "COMP309":
        course = "COMP309"
    elif chosen_course == "2" or chosen_course == "SWEN325":
        course = "SWEN325"
    elif chosen_course == "3" or chosen_course == "SWEN324":
        course = "SWEN324"
    elif chosen_course == "4" or chosen_course == "ENGR302":
        course = "ENGR302"
    else:
        return

    # get lecture number
    print("Enter lecture number:")
    num = input(">")

    # exec launcher script
    script = "python blank_lecture_slide_generator.py {0} {1}".format(course, num)
    print(script)
    os.system(script)

    print("Done")

    # I removed instead of uncommenting the "open in editor?" prompt here - check git history or see above

    return


def show_todos():
    """
    execute recursive GREP for "TODO" strings in wiki folder
    """
    os.chdir(config['wiki']['wiki_root'])
    os.system("grep -r \"TODO\" --include \\*.md")


def show_importants():
    """
    execute recursive GREP for "IMPORTANT" strings in wiki folder
    """
    os.chdir(config['wiki']['wiki_root'])
    os.system("grep -r \"IMPORTANT\" --include \\*.md")


def main():
    while True:
        print("""
Choose task:
    (1) New Lecture (from pdf)
    (2) New Lecture (blank)
    (3) Open text editor 
    (4) auto-commit wiki 
    (5) git status
    (6) open regular chrome tabs
    (7) list TODOs in wiki
    (8) list IMPORTANTs in wiki
    (9) exit""")
        response = input(">")
        if response == "1":
            new_lecture()
        elif response == "2":
            new_lecture_empty()
        elif response == "3":
            open_editor()
        elif response == "4":
            commit_wiki()
        elif response == "5":
            show_git_status()
        elif response == "6":
            open_chrome_tabs()
        elif response == "7":
            show_todos()
        elif response == "8":
            show_importants()
        elif response == "9":
            return
        else:
            print("unknown value")


if __name__ == '__main__':
    main()
