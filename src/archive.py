'''Convert all dashcam .MOV files into .MP4 files'''
import os
import subprocess

# Local cache process
#FOLDER = "C:\\workspace\\archive\\Dashcam24102701\\1"
#FOLDER = "C:\\workspace\\Dashcam\\1"
#FILTER = ""
#SUFFIX = "_local.mp4"

# Archive cache process
#FOLDER = "c:\\workspace\\footage"
FOLDER = "c:\\workspace\\Dashcam\\1"
FILTER = "-filter:v fps=1"
SUFFIX = "_archive.mp4"

files = os.listdir(FOLDER)

for file in files:
    if file.endswith(".MTS"):
        outFile = file.replace(".MTS", SUFFIX)
    elif file.endswith(".mkv"):
        outFile = file.replace(".mkv", SUFFIX)
    elif file.endswith(".MOV"):
        outFile = file.replace(".MOV", SUFFIX)
    elif file.endswith(".MP4"):
        if file.endswith("_archive.mp4"):
            continue
        if file.endswith("_local.mp4"):
            continue
        if file.endswith(SUFFIX):
            continue

        outFile = file.replace(".MP4", SUFFIX)
    else:
        continue

    if outFile in files:
        continue

    inPath=f"{FOLDER}\\{file}"
    outPath=f"{FOLDER}\\{outFile}"
    print (f'ffmpeg -i "{inPath}" {FILTER} "{outPath}"')
    subprocess.run(f'ffmpeg -i "{inPath}" {FILTER} "{outPath}"', check=True)

    ctime = os.path.getctime(inPath)
    utime = os.path.getmtime(inPath)
    os.utime(outPath, (ctime, utime))
