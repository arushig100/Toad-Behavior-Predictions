import csv
import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description="Convert a directory of videos into 10fps")
parser.add_argument("input_directory", type=str, help = "path to directory with videos (ends with a /)")
parser.add_argument("output_directory", type=str, help = "path to output directory (ends with a /)")
args = parser.parse_args()

def convert_to_10fps(input_directory_path, output_directory_path):
    # if the output directory does not already exist, create it
    if not os.path.exists(output_directory_path):
        os.mkdir(output_directory_path)

    input_dir = os.fsencode(input_directory_path)
    # iterate through files in input directory
    for file in os.listdir(input_dir):
        file_name = os.fsdecode(file)
        if file_name[-4:] == ".mp4":
            os.system("ffmpeg -i " + input_directory_path + file_name + " -r 10 -y " + output_directory_path + file_name)

# Call to the convert_to_10fps function with directory path to videos
convert_to_10fps(args.input_directory, args.output_directory)
