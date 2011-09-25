import os, sys
import shutil
import Image, ImageFile

try:
    maskimage = Image.open('mask/2272x1704.png')
except IOError:
    print "cannot open mask file"

for infile in os.listdir('infiles/'):
    try:
        inimage = Image.open('infiles/' + infile)
    except IOError:
        print "Cannot open", infile
    maskimage.paste(inimage)
    maskimage.save('outfiles/' + infile, 'PNG')
