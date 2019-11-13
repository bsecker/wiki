"""
Simple script to generate a markdown file with only basic templates and no images from pdf being inserted.

see pdf_lecture_slide_generator.py for a script that generates markdown using an existing pdf

"""
import argparse
import configparser
import datetime
import os

# read the configuration file
config = configparser.ConfigParser()
config.read("config.cfg")


def main(course, lecture_num, output_file=None):
    now = datetime.datetime.now().strftime("%d/%m/%y")
    markdown_file_string = "# Lecture {0}: \n({1}) \n\n".format(lecture_num, now)

    filename = "lecture_{0}.md".format(lecture_num)

    if output_file is None:
        output_path = os.path.join(config["wiki"]["wiki_root"], "Uni", course, "Lectures")

        # make directory if it doesnt exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        output_file = os.path.join(output_path, filename)

        if os.path.exists(output_file):
            print("Error: File exists already! Aborting.")
            return

    with open(output_file, 'w') as f:
        f.write(markdown_file_string)

    print("wrote to " + output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("course", help="course",
                        choices=['COMP309', 'SWEN325', 'ENGR302', 'SWEN324'])  # TODO replace with proper course names
    parser.add_argument("lecture_num", help="lecture number (used as ID)")
    parser.add_argument("--output-file", help="output markdown file")

    args = parser.parse_args()

    main(args.course, args.lecture_num, output_file=args.output_file)
