#-------------------------------------------------------------------------------
# Name:        add-watermark
# Purpose:     Add custom watermark to pdfs
#
# Author:      Charles Lomboni
#
# Created:     27/08/2019
# Updated:     09/03/2020
#
# Copyright:   (c) Charles Lomboni 2019
# Licence:     MIT
#-------------------------------------------------------------------------------

import PyPDF2
import argparse
import os

folderToSave = "Done"
splitSlash = ""

def getargs():
    parser = argparse.ArgumentParser()

    parser.usage
    parser.add_argument("-w", "--watermarkFile", help="Watermark.pdf to merge")
    parser.add_argument("-d", "--directory", help="Path with all pdf files")
    parser.add_argument("-s", "--opSystem", help="Operation System by default is linux, if you are runing on windows use .: -s win")


    return parser.parse_args()


def mergePages(pdfReader, watermarkFile, pdfWriter, wFile, number):
    currentPage = pdfReader.getPage(number)

    pdfWatermarkerReader = PyPDF2.PdfFileReader(wFile)
    currentPage.mergePage(pdfWatermarkerReader.getPage(0))

    pdfWriter.addPage(currentPage)

    return pdfWriter


def insertWatermark(watermarkFile, originalFile, oneFile=False, opSystem="lin"):

    originalFile = open(originalFile,'rb')
    pdfReader = PyPDF2.PdfFileReader(originalFile)
    wFile = open(watermarkFile, 'rb')
    pdfWriter = PyPDF2.PdfFileWriter()
    maxLen = pdfReader.numPages

    count = 0
    while (count < maxLen):
        pdfWriter = mergePages(pdfReader, watermarkFile, pdfWriter, wFile, count)
        count += 1

    if (oneFile == True):
        outputName = originalFile.name
    else:
        splitLen = 0
        splitLen = len(str(originalFile.name).split(splitSlash))
        outputName = str(originalFile.name).split(splitSlash)[splitLen-1]


    pathToSave = str(os.path.dirname(originalFile.name) + splitSlash + folderToSave)
    if (os.path.exists(pathToSave) == False):
        os.mkdir(pathToSave)


    resultPdfFile = open(pathToSave + splitSlash + outputName, 'wb')
    pdfWriter.write(resultPdfFile)
    originalFile.close()
    wFile.close()
    resultPdfFile.close()


def getAllPdfFiles(directory):
    files = []
    for r, d, f in os.walk(directory):
        for file in f:
            if '.pdf' in file:
                files.append(os.path.join(r, file))

    return files

def main():

    args = getargs()

    watermark = args.watermarkFile
    directory = args.directory
    opSystem  = args.opSystem

    global splitSlash
    splitSlash = ("/", "\\")["win" == opSystem]

    if (str(directory).find('.pdf') == -1):
        files = getAllPdfFiles(directory)
        for f in files:
            insertWatermark(watermark, f, opSystem=opSystem)
            print('=> Saved file: [ ' + folderToSave + splitSlash + f.split(splitSlash)[len(f.split(splitSlash))-1] + ' ]')
    else:
        insertWatermark(watermark, directory, oneFile=True)
        print('=> Saved file: [ ' + folderToSave + splitSlash + directory + ' ]')



if __name__ == '__main__':
    main()