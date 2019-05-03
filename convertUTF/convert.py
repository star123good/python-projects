# 2016-2017 Soverance Studios.
# Scott McCutchen

# This file will search all files and folders within a given directory, and use Notepad++ to convert their encoding to UTF-8 without Byte Order Marks
#
# This file must be run using the PythonScript plugin from within Notepad++, which is available through the Notepad++ Plugin Manager
#
# You must have Python 2.7 installed
#
# Additionally, this script can only exist and be run from within the Notepad++ user's working directory, the default of which is here:
# Note that selecting "New Script" from within the PythonScript plugin will automatically default to this save location

#  .. USER DIRECTORY\AppData\Roaming\Notepad++\plugins\Config\PythonScript\scripts

import os;
import sys;
# from commands import *
# from Npp import notepad

filePathSrc="aaa" # Path to the folder with files to convert

for root, dirs, files in os.walk(filePathSrc):
    for fn in files:
        if fn[-2:] == '.h' or fn[-5:] == '.html': # Specify file types, taking care to change the fn[number] to correspond to length of the file's extension including the .
             # notepad.open(root + "\\" + fn)
             # notepad.runMenuCommand("Encoding", "Encode in Shift-JIS")
             # notepad.runMenuCommand("Encoding", "Convert to UTF-8")
             # notepad.save()
             # notepad.close()
             # print(root + "/" + fn)
             os.system("iconv -f EUC-JP -t UTF-8 %s > converted/%s" % ((root + "/" + fn), (root + "/" + fn)))