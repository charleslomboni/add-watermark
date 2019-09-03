#-------------------------------------------------------------------------------
# Name:        add-watermark
# Purpose:     Add custom watermark to pdfs
#
# Author:      Charles Lomboni
#
# Created:     27/08/2018
# Copyright:   (c) Charles Lomboni 2018
# Licence:     MIT
#-------------------------------------------------------------------------------

import PyPDF2
import argparse
import os

def getargs():
    parser = argparse.ArgumentParser()

    parser.usage
    parser.add_argument("-w", "--watermarkFile", help="Watermark.pdf to merge")
    parser.add_argument("-d", "--directory", help="Path with all pdf files")
    

    return parser.parse_args()


def mergePages(pdfReader, watermarkFile, pdfWriter, wFile, number):
    currentPage = pdfReader.getPage(number)

    pdfWatermarkerReader = PyPDF2.PdfFileReader(wFile)
    currentPage.mergePage(pdfWatermarkerReader.getPage(0))

    pdfWriter.addPage(currentPage)

    return pdfWriter


def insertWatermark(watermarkFile, originalFile, oneFile=False):
    
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
        outputName = str(originalFile.name).split('/')[1]

    pathToSave = str(os.getcwd() + '/done')
    if (os.path.exists(pathToSave) == False):
        os.mkdir(pathToSave)


    resultPdfFile = open(pathToSave+'/'+outputName, 'wb')
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

    if (str(directory).find('.pdf') == -1):
        files = getAllPdfFiles(directory)
        for f in files:
            insertWatermark(watermark, f)
            print('=> Saved file: [ done/' + f.split('/')[1] + ' ]')
    else:
        insertWatermark(watermark, directory, oneFile=True)
        print('=> Saved file: [ done/' + directory + ' ]')



if __name__ == '__main__':
    main()