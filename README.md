# Toad-Behavior-Predictions

### 1. Install deepethogram.

Install deepethogram using the instructions here: https://github.com/jbohnslav/deepethogram/blob/master/docs/installation.md, which involve: 

- Install Anaconda
- Create a new anaconda environment: `conda create --name deg python=3.7`
- Activate your environment: `conda activate deg`
- Install PySide2: `conda install -c conda-forge pyside2==5.13.2`
- Install PyTorch: Use this link for official instruction (command differs based on OS) - https://pytorch.org/
- Run the command: `pip install deepethogram`

### 2. Download this Github Repository (the code files).

### 3. Upload all videos (you want predictions for) to a directory on your computer.

### 4. Convert all videos to 10fps.
Convert all videos to 10fps by running the following command:
```
python3 convert10fps.py input_directory_path output_directory_path
```
`input_directory_path` should be the path to a directory of all the videos you want to be converted to 10fps. The path should end with a “/”

`output_directory_path` should be the path to a directory (initially empty or nonexistent) where the videos converted to 10fps will be put. If the directory does not exist, it will be created. The path should end with a “/”

Example command: `python3 convert10fps.py /Users/arushigupta/Downloads/2022-04-05/ /Users/arushigupta/Downloads/2022-04-05_10fps/`

### 5. Add the videos to the project directory.

Add videos to the project directory (i.e., the directory called toad in the repository) by running the following command:

```python3 addvideos.py videos_directory_path project_directory_path```

`videos_directory_path` should be the path to a directory of all the videos you want to generate predictions for. These videos should have already been converted to 10fps. The path should end with a “/”

`project_directory_path` should be the path to the project directory (i.e., the toad directory in Google Drive). The path should end with a “/”

Example command: `python3 addvideos.py /Users/arushigupta/Downloads/2022-04-05_10fps/ /Users/arushigupta/Downloads/toad/`

### 6. Run inference.
Run inference by running the following command: 
```python3 inference.py project_directory_path```

`project_directory_path` should be the path to the project directory (i.e., the toad directory in Google Drive). The path should end with a “/”

Example Command: `python3 inference.py /Users/arushigupta/Downloads/toad/`

### 7. Generate predictions.
Generate a CSV file containing the predictions by running the following command: 
```python3 genpredictions.py project_directory_path videos_directory_path output_directory_path```

`project_directory_path` should be the path to the project directory (i.e., the toad directory in Google Drive). The path should end with a “/”

`videos_directory_path` should be the path to a directory of all the videos you want to generate predictions for. These videos should have already been converted to 10fps. The path should end with a “/”

`output_directory_path` should be the path to the directory in where you want the CSV file with the predictions to be put. The path should end with a “/”. Note that you should differ the output directory path each time you follow these steps for generating predictions because the CSV file generated is always called predictions.csv.

Example Command: `python3 genpredictions.py /Users/arushigupta/Downloads/toad/ /Users/arushigupta/Downloads/2022-04-05_10fps/ /Users/arushigupta/Downloads/`

### 8. View predictions.
You can view the predictions in the CSV file called predictions.csv in the output directory specified by `output_directory_path` in Step 6.

### To generate predictions for more folders of videos, do Steps 3-8 again and make sure the conda environment is activated.
To make sure the conda environment is activated, run `conda activate deg`
