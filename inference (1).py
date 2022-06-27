import multiprocessing
from deepethogram import configuration, postprocessing, projects, utils
from deepethogram.debug import print_dataset_info
from deepethogram.flow_generator.train import flow_generator_train
from deepethogram.feature_extractor.train import feature_extractor_train
from deepethogram.feature_extractor.inference import feature_extractor_inference
from deepethogram.sequence.train import sequence_train
from deepethogram.sequence.inference import sequence_inference
import os
from pathlib import Path
import csv
import os
import subprocess
from collections import deque
import json
import logging
import yaml
import random
import argparse

parser = argparse.ArgumentParser(description="Run feature extractor inference and sequence inference")
parser.add_argument("project_directory", type=str, help = "path to project directory (ends with a /)")
args = parser.parse_args()

def run_inference(project_path):

    # Feature extractor inference
    preset = 'deg_f'
    n_cpus = multiprocessing.cpu_count()

    cfg = configuration.make_feature_extractor_inference_cfg(project_path=project_path, preset=preset)
    cfg.flow_generator.weights = project_path + 'models/220329_211116_flow_generator_train/checkpoint.pt'
    cfg.feature_extractor.weights = project_path + 'models/220618_160634_feature_extractor_train/checkpoint.pt'
    cfg.inference.overwrite = False
    # make sure errors are thrown
    cfg.inference.ignore_error = False
    cfg.compute.num_workers = 2
    feature_extractor_inference(cfg)

    # Sequence inference
    cfg = configuration.make_sequence_inference_cfg(project_path)
    cfg.sequence.weights = 'latest'
    cfg.compute.num_workers = n_cpus
    cfg.inference.overwrite = False
    cfg.inference.ignore_error = False
    sequence_inference(cfg)
    cfg = configuration.make_postprocessing_cfg(project_path=project_path)
    postprocessing.postprocess_and_save(cfg)

run_inference(args.project_directory)