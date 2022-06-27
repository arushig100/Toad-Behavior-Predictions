
import multiprocessing
from deepethogram import configuration, postprocessing, projects, utils
from deepethogram.debug import print_dataset_info
from deepethogram.flow_generator.train import flow_generator_train
from deepethogram.feature_extractor.train import feature_extractor_train
from deepethogram.feature_extractor.inference import feature_extractor_inference
from deepethogram.sequence.train import sequence_train
from deepethogram.sequence.inference import sequence_inference
from pathlib import Path
import csv
import os
import subprocess
from collections import deque
import json
import logging
import yaml
import random
from omegaconf import OmegaConf
import argparse


parser = argparse.ArgumentParser(description="Add video to project directory")
parser.add_argument("videos_directory", type=str, help = "path to directory with videos that are all 10fps (ends with a /)")
parser.add_argument("project_directory", type=str, help = "path to project directory (ends with a /)")
args = parser.parse_args()


# Adding videos to directory
mode = 'symlink'

def add_videos(videos_directory_path, project_directory_path):
    list_of_movies = []
    directory = os.fsencode(videos_directory_path)
    for file in os.listdir(directory):
        file_name = os.fsdecode(file)
        list_of_movies.append(videos_directory_path+file_name)

    with open(project_directory_path+ 'project_config.yaml', 'r') as f: # Edit to contain the path to the project directory
        project_config_dict = yaml.load(f, Loader=yaml.Loader)
        for movie_path in list_of_movies:
            try:
                print("Adding video:", movie_path, "\n")
                projects.add_video_to_project(project_config_dict, movie_path, mode=mode)
            except ValueError:
                print("Error adding video to project", movie_path, "\n")
                pass

add_videos(args.videos_directory, args.project_directory)
