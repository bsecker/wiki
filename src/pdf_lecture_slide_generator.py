"""
PDF Handout to markdown file generator.
Usage:

./pdf_lecture_slide_generator input.pdf output.md [--no-image-directory]

Will turn a pdf slides printout into a series of images and put it in images/ relative to output.md. Output.md
will contain a header and links to images

TODO:
 - Add support for splitting up groups of images per slides
 - add support for opening URLS

@author Benjamin Secker
@email benjamin.secker@gmail.com
"""
import argparse
import tempfile
import configparser
import re
import requests

import pdf2image
import os
import datetime
import tempfile

from PIL import PngImagePlugin

# read the configuration file
config = configparser.ConfigParser()
config.read("config.cfg")


def main(input_path: str,
         course: str,
         lecture_num,
         output_file=None,
         password=None,
         title="",
         save_image_dir=False):
    # if output_file is none, figure file path out based on course.
    # otherwise, save to given filename
    if not output_file:

        # if the title is given, convert to a filename friendly title
        converted_title = "-" + title.lower().replace(" ", "-")

        filename = "lecture-{:02d}{}.md".format(int(lecture_num), "" if not title else converted_title)
        output_path = os.path.join(config["wiki"]["wiki_root"], "Uni", course, "Lectures")

        # make directory if it doesnt exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_file = os.path.join(output_path, filename)

    # images are relative from output file path
    if save_image_dir:
        images_path = os.path.dirname(os.path.abspath(output_file))
    else:
        images_path = os.path.join(os.path.dirname(os.path.abspath(output_file)), "images",
                                   "lecture-{:02d}".format(int(lecture_num)))

        # make images directory
        if not os.path.exists(images_path):
            os.mkdir(images_path)

    print("saving images to ", images_path)

    url = None

    # if URL, download first
    if is_url(input_path):

        url = input_path

        print("URL detected, downloading...")

        # download the URL to temporary file
        response = requests.get(input_path)

        # detect filetype from MIME-TYPE of request
        content_type = response.headers['content-type']
        if content_type == 'application/pdf':
            filetype = ".pdf"
        elif content_type == "application/vnd.ms-powerpoint":
            filetype = ".ppt"
        elif content_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
            filetype = ".pptx"
        else:
            print("couldn't figure out type of downloaded file. aborting")
            return

        print("downloaded {0}.".format(filetype))

        # write temporary file
        temp = tempfile.NamedTemporaryFile(suffix=filetype)
        temp.write(response.content)

        # set input path to the temporary file
        input_path = temp.name

    # convert the image files

    # if ppt, convert to pdf first using unoconv
    if input_path.endswith(".ppt") or input_path.endswith(".pptx"):
        # replace pptx with ppt, then ppt with pdf to always ensure pdf
        renamed_path = input_path.replace(".pptx", ".ppt").replace(".ppt", ".pdf")

        print("renamed from {0} to {1}".format(input_path, renamed_path))

        # unoconv doesn't support writing to a file, so pipe to a file manually
        os.system("unoconv -f pdf --stdout \"{0}\" > \"{1}\"".format(input_path, renamed_path))

        # finally rename the path
        input_path = renamed_path

    print("converting PDF...")
    with tempfile.TemporaryDirectory() as path:
        images = pdf2image.convert_from_path(
            pdf_path=input_path,
            dpi=75,
            output_folder=path,
            fmt="png",
            thread_count=4,
            userpw=password,
        )
    print("done.")

    now = datetime.datetime.now().strftime("%d/%m/%y")
    markdown_file_string = "# Lecture {0}: {1}\n({2}) \n\n".format(lecture_num, title, now)

    # Append URL
    if url:
        markdown_file_string += "[Online lecture slides link]({0})\n\n".format(url)

    # name and save each file to directory, and append to markdown
    image: PngImagePlugin.PngImageFile
    for image_num, image in enumerate(images):
        # get filenames and paths
        image_name = "lecture_{0}_{1}.png".format(lecture_num, image_num)
        image_path = os.path.join(images_path, image_name)

        # save to file
        image.save(image_path)

        # save to markdown
        markdown_file_string += "![image]({0})\n".format("images/lecture-{0:02d}/{1}".format(int(lecture_num), image_name))

        # add note 
        markdown_file_string += "### Slide {0} notes \n\n".format(image_num)

    # write markdown to file
    # save to a file if given otherwise save to wiki
    with open(output_file, 'a') as f:
        f.write(markdown_file_string)


def is_url(_str):
    """return true if the str input is a URL"""
    ur = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', _str)
    return len(ur) > 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input pdf file or url")
    parser.add_argument("course", help="course",
                        choices=['COMP309', 'SWEN325', 'ENGR302', 'SWEN324'])  # TODO replace with config
    parser.add_argument("lecture_num", help="lecture number (used as ID)")
    parser.add_argument("--output-file", help="output markdown file")
    parser.add_argument("--password", help="pdf file password")
    parser.add_argument("--title", help="Lecture title")
    parser.add_argument("--no-image-directory",
                        action="store_true",
                        help="save images to same directory as output file, instead of images/")

    args = parser.parse_args()

    main(args.input, args.course, args.lecture_num,
         output_file=args.output_file, password=args.password,
         save_image_dir=args.no_image_directory,
         title=args.title)
