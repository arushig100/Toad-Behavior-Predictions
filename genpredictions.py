import csv
import os
import subprocess
import logging
import multiprocessing
import argparse

behaviors = ['subject out of view',
             'climb',
             'in - entered pen',
             'hop',
             'rest',
             'exit - escaped pen']


# given a file name (for a video mp4 file) and the directory it is in, returns the fps of the file
def get_fps(file_name, directory_string):
    directory = os.fsencode(directory_string)
    for file in os.listdir(directory):
        filenamedir = os.fsdecode(file)
        if filenamedir == file_name:

            os.chdir(directory_string)
            result = subprocess.run(
                [
                    'ffprobe',
                    '-v',
                    'error',
                    '-show_entries',
                    'format=duration',
                    '-of',
                    'default=noprint_wrappers=1:nokey=1',
                    file
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            result2 = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-select_streams",
                    "v",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    "-show_entries",
                    "stream=r_frame_rate",
                    file_name,
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

            result2_string = result2.stdout.decode('utf-8').split()[0].split('/')
            fps = float(result2_string[0])/float(result2_string[1])
            return fps


# given a video name and the fps of the video, prints out the predictions
def convert_predictions(project_path, vid_name, fps):
    print(vid_name, '\n') # print out vid_name

    vid_name = vid_name[:-4] # get rid of the .mp4 at the end
    on_behavior = [-1,-1,-1,-1,-1,-1] # list that stores whether we are currently on a certain behavior (if so stores the start frame, otherwise -1)
    intervals_for_behaviors = {}
    for i in range(0,6):
        intervals_for_behaviors[i] = []

    # go to directory of vid_name
    os.chdir(project_path+"DATA/"+vid_name)
    # open CSV predictions file
    with open(vid_name+"_predictions.csv", 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        num_line = -1
        row_count = sum(1 for row in csv_reader)-2
        csv_file.seek(0) # return pointer to row 0
        csv_reader = csv.reader(csv_file, delimiter = ",")

        # goes through csv file and stores intervals in intervals_for_behaviors
        for line in csv_reader:
            # first line of predictions is line 0 (second line in csv file)
            if num_line >=0:
                for i in range(1,7):
                    # starting interval
                    if line[i] == "1" and on_behavior[i-1] == -1:
                        on_behavior[i-1] = num_line/float(fps) # divide by fps to get it in seconds
                    # ending interval (not on last line)
                    if line[i] == "0" and on_behavior[i-1] != -1:
                        intervals_for_behaviors[i-1].append([on_behavior[i-1], (num_line-1)/float(fps)]) # divide by fps to get it in seconds
                        on_behavior[i-1] = -1
                    # ending interval (on last line)
                    if num_line == row_count and on_behavior[i-1] != -1:
                        intervals_for_behaviors[i-1].append([on_behavior[i-1], (num_line)/float(fps)]) # divide by fps to get it in seconds
            num_line+=1
        return intervals_for_behaviors


def convert_directory(project_path, directory_path, output_directory):
    directory = os.fsencode(directory_path)
    os.chdir(output_directory)
    with open("predictions.csv", "a") as predictions_file:
        writer = csv.writer(predictions_file)
        header = ["File"]
        for beh in behaviors:
            header.append(beh)
        writer.writerow(header)

        for file in os.listdir(directory):
            file_name = os.fsdecode(file)
            if file_name[-4:] == ".mp4":
                intervals_for_behaviors = convert_predictions(project_path, file_name,10)
                prediction = [file_name]
                for i in range(0,6):
                    prediction.append(intervals_for_behaviors[i])
                writer.writerow(prediction)


parser = argparse.ArgumentParser(description="Convert predictions")
parser.add_argument("project_directory", type=str, help = "path to project directory (ends with a /)")
parser.add_argument("videos_directory", type=str, help = "path to directory with videos that are all 10fps (ends with a /)")
parser.add_argument("output_directory", type=str, help = "path to directory you would want to contain the predictions csv")
args = parser.parse_args()



convert_directory(args.project_directory, args.videos_directory, args.output_directory)

