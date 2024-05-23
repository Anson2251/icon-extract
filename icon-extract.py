#! /usr/bin/python3

# Extract the icon from a Windows executable and convert it to an Apple Icon Image.
# Copyright (C) 2024-present  Heyan Zhu (Anson2251)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import uuid
import subprocess
import re

def createTmpDict() -> str:
    name = uuid.uuid4()
    mkdirCommand = f"mkdir /tmp/{name}"
    subprocess.run(mkdirCommand, shell=True)
    return f"/tmp/{name}"

def removeTmpDir(workDir: str) -> None:
    rmCommand = f"rm -rf {workDir}"
    subprocess.run(rmCommand, shell=True)

def extract(inputfile: str, workDir: str) -> str:
    # wrestool -x -t 14 source.exe > output.ico:
    inputFileDir = f"{workDir}/{inputfile.split("/").pop()}-icon.ico"
    extractCommand = f"wrestool -x -t 14 {inputfile} > {inputFileDir}"
    subprocess.run(extractCommand, shell=True)
    return inputFileDir

def getIcoFileComponents(inputFile: str) -> str:
    command = f"icotool -l {inputFile}"
    output = subprocess.check_output(command, shell=True, text=True)
    lines = output.splitlines()

    pattern = r"--icon --index=(\d+) --width=(\d+) --height=(\d+)"
    iconInfo = {}

    matches = re.findall(pattern, output)

    for match in matches:
        index, width, height = match
        iconInfo[index] = {"width": int(width), "height": int(height)}

    return iconInfo

def createSizeDiff(sizes, sizesNeeded):
    sizeDiff = [];
    for i in range(len(sizes)):
        cell = []
        for actualSize in sizesNeeded:
            cell.append(abs(actualSize - sizes[i]))
        sizeDiff.append(cell)

    return sizeDiff

def determineBestSource(sizeDiff, sizesNeeded, size) -> int:
    dataIndex = sizesNeeded.index(size);
    sizeDiff = [sizeDiff[i][dataIndex] for i in range(len(sizeDiff))]; # extract the differences between the sizes of each exist image and the desired size
    return sizeDiff.index(min(sizeDiff))

def createIcnsFile(inputFiles, sizes, workDir: str, name: str, outputfile: str) -> None:
    # sips -z 32 32 png_icons/extracted_icon.png --out MyApp.iconset/icon_16x16.png
    sizesNeeded = [16, 32, 64, 128, 256, 512, 1024]
    sizeDiff = createSizeDiff(sizes, sizesNeeded)

    iconsetDir = f"{workDir}/{"".join(name.replace('.icns', ''))}.iconset"
    mkdirCommand = f"mkdir {iconsetDir}"
    subprocess.run(mkdirCommand, shell=True)

    for size in sizesNeeded:
        sourceIndex = determineBestSource(sizeDiff, sizesNeeded, size)
        command = f"sips -z {size} {size} {inputFiles[sourceIndex]} --out {iconsetDir}/icon_{size}x{size}.png > /dev/null"
        subprocess.run(command, shell=True)

    command = f"iconutil -c icns {iconsetDir} -o {outputfile}"
    subprocess.run(command, shell=True)

def convertIcoToPng(inputFile: str, icoInfo, workDir: str):
    # icotool -i 1 -x o.ico
    sizes = []
    for key, value in icoInfo.items():
        sizes.append(int(value["width"]))
        command = f"icotool -i {key} -x {inputFile} -o {workDir}/extracted_icon_{value["width"]}.png"
        subprocess.run(command, shell=True)

    return [f"{workDir}/extracted_icon_{str(s)}.png" for s in sizes], sizes

workDir = createTmpDict()

def main():
    parser = argparse.ArgumentParser(description="Extract the icon from a Windows executable and convert it to an Apple Icon Image.")
    
    parser.add_argument("inputfile", type=str, help="The executable to extract the icon from")
    parser.add_argument("-n", "--name", type=str, default="output",help="The name of the icon", required=False)
    parser.add_argument("-o", "--output", type=str, help="The output icon", required=False)
    
    args = parser.parse_args()

    currentDir = subprocess.check_output("pwd", shell=True, text=True).strip()
    inputfile = args.inputfile
    name = args.name

    outputFileName = str(args.output if args.output else f"{name}.icns")
    outputfile = f"{currentDir}/{outputFileName}"
    
    icoFile = extract(inputfile, workDir)
    icoInfo = getIcoFileComponents(icoFile)
    files, sizes = convertIcoToPng(icoFile, icoInfo, workDir)

    createIcnsFile(files, sizes,  workDir, name, outputfile)
    
if __name__ == "__main__":
    try:
        main()
    finally:
        removeTmpDir(workDir)
