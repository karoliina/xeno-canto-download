#!/usr/bin/env/python
#
# A script to download bird sound files from the www.xeno-canto.org archives.
#
# Usage: python xcdl.py searchTerm1 searchTerm2 ... searchTermN
#
# The program downloads all the files found with the search terms into
# subdirectory sounds.
#
# Karoliina Oksanen <hkoksanen@gmail.com>, 2014

import urllib
import sys
import re
import os

# returns the Xeno Canto catalogue numbers for the given search terms.
# @param searchTerms: list of search terms
# http://www.xeno-canto.org/explore?query=common+snipe
def read_numbers(searchTerms):
    i = 1 # page number
    numbers = []
    while True:
        page = urllib.urlopen("http://www.xeno-canto.org/explore?pg={0}&query={1}".format(i,
            '+'.join(searchTerms)))
        newResults = re.findall(r"/(\d+)/download", page.read())
        if(len(newResults) > 0):
            numbers.extend(newResults)
        # check if there are more than 1 page of results (30 results per page)
        if(len(newResults) < 30):
            break
        else:
            i += 1 # move onto next page

    return numbers 

# returns the filenames for all Xeno Canto bird sound files found with the given
# search terms.
# @param searchTerms: list of search terms
def read_filenames(searchTerms):
    i = 1 # page number
    filenames = []
    while True:
        page = urllib.urlopen("http://www.xeno-canto.org/explore?pg={0}&query={1}".format(i,
            '+'.join(searchTerms)))
        newResults = re.findall(r"data-xc-filepath=\'(\S+)\'", page.read())
        if(len(newResults) > 0):
            filenames.extend(newResults)
        # check if there are more than 1 page of results (30 results per page)
        if(len(newResults) < 30):
            break
        else:
            i += 1 # move onto next page

    return filenames

# creates the subdirectory sounds if necessary, and downloads all sound files
# found with the search terms into that directory. inserts the XC catalogue
# number in front of the file name, otherwise preserving original file names.
def download(searchTerms):
    # create sounds directory
    if not os.path.exists("sounds"):
        print "Creating subdirectory \"sounds\" for downloaded files..."
        os.makedirs("sounds")
    filenames = read_filenames(searchTerms)
    if len(filenames) == 0:
        print "No search results."
        sys.exit()
    numbers = read_numbers(searchTerms)
    # regex for extracting the filename from the file URL
    fnFinder = re.compile('\S+/+(\S+)')
    print "A total of {0} files will be downloaded.".format(len(filenames))
    for i in range(0, len(filenames)):
        localFilename = numbers[i] + "_" + fnFinder.findall(filenames[i])[0]
        # some filenames in XC are in cyrillic characters, which causes them to
        # be too long in unicode values. in these cases, just use the ID number
        # as the filename.
        if(len("sounds/" + localFilename) > 255):
            localFilename = numbers[i]
            print "Downloading " + localFilename
        urllib.urlretrieve(filenames[i], "sounds/" + localFilename) 

def main(argv):
    if(len(sys.argv) < 2):
        print "Usage: python xcdl.py searchTerm1 searchTerm2 ... searchTermN"
        print "Example: python xcdl.py common snipe"
        return
    else:
        download(argv[1:len(argv)])

if __name__ == "__main__":
    main(sys.argv)
