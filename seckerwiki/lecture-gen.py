#!/usr/bin/env python3
import argparse
import tempfile
import re
import requests
import os
from datetime import date

import pdf2image
from PIL import PngImagePlugin
import yaml

def convert_to_pdf(input_path):
    """
    Use external tools to convert the powerpoint file to a pdf.
    :return path of converted file
    """
    path, extension = os.path.splitext(input_path)

    if extension not in ['.ppt', '.pptx']:
        raise ValueError("{0} not a valid powerpoint extension".format(extension))

    renamed_path = path + ".pdf"

    # unoconv doesn't support writing to a file, so pipe to a file
    print("Powerpoint file detected, converting...")
    os.system("unoconv -f pdf --stdout \"{0}\" > \"{1}\"".format(input_path, renamed_path))
    print("converted from {0} to {1}".format(input_path, renamed_path))

    return renamed_path


def download_file(url):
    """
    Download and return temporary file
    """
    print("url detected, downloading...")

    response = requests.get(url)

    # detect file type from MIME-TYPE of request
    content_type = response.headers['content-type']
    if content_type == 'application/pdf':
        file_type = ".pdf"
    elif content_type == "application/vnd.ms-powerpoint":
        file_type = ".ppt"
    elif content_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
        file_type = ".pptx"
    else:
        print("couldn't figure out type of downloaded file. aborting")
        raise

    print("downloaded {0}".format(file_type))

    # write to temporary file
    temp = tempfile.NamedTemporaryFile(suffix=file_type)
    temp.write(response.content)

    return temp


def is_url(_str):
    """return true if the str input is a URL."""
    ur = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', _str)
    return len(ur) > 0


def create_filename(lecture_num, title):
    """
    :return lecture filename
    """
    return "lecture-{:02d}{}.md".format(int(lecture_num), "" if not title else '-'+ title.lower().replace(" ", "-"))


def create_markdown_header(lecture_num, title, url):
    now = date.today().isoformat()
    url_link = "[Online lecture slides link]({0})".format(url) if url else ""
    return "# Lecture {0}: {1}\n({2})\n\n{3}\n\n".format(lecture_num, title, now, url_link)


def get_tri_from_course(course, courses):
    """
    Given a courses dict, return the trimester of the :param course
    """
    for tri in courses:
        for _course in courses[tri]:
            if course == _course:
                return tri


def get_wiki_folder(config, lecture_num, course, config):
    """
    Return tuple of (lecture file location, markdown images path)
    """

    tri = get_tri_from_course(course, config['courses'])
    lecture_path = os.path.join(config['wiki-root'], "Uni", tri.capitalize(), course, "Lectures")
    images_path = os.path.join(lecture_path, "images", "Lecture-{:02d}".format(int(lecture_num)))

    return [lecture_path, images_path]

def main(args):
    # load config file
    try:
        cfg_file = os.environ['WIKI_CONFIG'] if 'WIKI_CONFIG' in os.environ else os.path.expanduser('~/.personal.yml')
        with open(cfg_file, 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)
    except FileNotFoundError:
        print("Config file not found. Have you ran `wiki setup`?")

    # combine the possible course selections from both tris
    courses = [item for key in cfg['courses'].keys() for item in cfg['courses'][key]]

    # Cache the downloaded file so it doesn't get deleted with GC
    downloaded = None

    # Download the file if script was provided a URL
    if is_url(args.pdf):
        downloaded = download_file(args.pdf)
        file = downloaded.name
        url = args.pdf
    else:
        file = args.pdf
        url = None

    # convert to pdf if it isn't one already
    extension = os.path.splitext(file)[1]
    pdf = convert_to_pdf(file) if extension in ['.ppt', '.pptx'] else file

    # convert the file to a series of images
    print("converting PDF to images...")
    with tempfile.TemporaryDirectory() as image_path:
        images = pdf2image.convert_from_path(
            pdf_path=pdf,
            dpi=60,
            output_folder=image_path,
            fmt="png",
            thread_count=4
        )
    print("done.")


    # Get paths
    lecture_path, images_path = get_wiki_folder(config, args.lecture_num, args.course, cfg)

    # create dirs if they don't exist
    if not os.path.exists(images_path):
        os.makedirs(images_path, exist_ok=True)

    # Create top of lecture page
    lecture_markdown = create_markdown_header(args.lecture_num, args.title, url)

    # Add images to subfolder and lecture page
    for image_num, image in enumerate(images):

        # get filenames and paths
        image_name = "lecture-{0}-{1}.png".format(args.lecture_num, image_num)
        image_path = os.path.join(images_path, image_name)

        # save to file
        image.save(image_path)

        # save to markdown
        lecture_markdown += "![image]({0})\n".format("images/Lecture-{0:02d}/{1}".format(int(args.lecture_num), image_name))

        # add note
        lecture_markdown += "### Slide {0} notes \n\n".format(image_num)

    # Finally, write out to the file
    with open(os.path.join(lecture_path, create_filename(args.lecture_num, args.title)), 'a') as f:
        f.write(lecture_markdown)

    print("Generated Lecture in {0}".format(lecture_path))

if __name__ == '__main__':
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", help="input pdf file or url")
    parser.add_argument("course", help="course", choices=courses)
    parser.add_argument("lecture_num", help="lecture number")
    parser.add_argument("--title", help="Lecture title")
    parser.add_argument("--blank", help="blank lecture")

    args = parser.parse_args()

    main()