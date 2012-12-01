# vim: set fileencoding=utf-8 :
# Mount and print functions
import os
import shutil
import subprocess
import time

camera_mount = "/media/NIKON D60"
camera_src = camera_mount + "/DCIM/100KM530"
printer = 'HP-Photosmart-C5280'
#printer = 'Kodak_ESP_5200_Series_AiO'
#printer = 'Brother-MFC-5840CN-USB'
do_camera = False
do_print = False

class UnboundCallbackError (UnboundLocalError):
	""" Callback function not set error. """
	pass

class Logger:
	_callback = None

	def setCallback(self, callback=None):
		type(self)._callback = callback

	def log(self, message):
		if self._callback != None:
			self._callback(message)
		else:
			raise UnboundCallbackError, "Callback function not set"

def mount_camera():
    if do_camera:
        if os.path.exists(camera_mount) and os.path.ismount(camera_mount):
            mounted = True
        else:
            mounted = not subprocess.call(['mount', camera_mount])
        return mounted
    else:
        return True

def get_camera_files():
    if do_camera:
        if os.path.exists(camera_src):
            for src_file in os.listdir(camera_src):
                shutil.move(camera_src + '/' + src_file, 'infiles/')

def umount_camera():
    if do_camera:
        if os.path.exists(camera_mount) and os.path.ismount(camera_mount):
            umounted = not subprocess.call(['umount', camera_mount])
        else:
            umounted = True
        return umounted
    else:
        return True

def print_image(filename, copies=1):
    if do_print:
        success = not subprocess.call(['lp', '-d', printer, '-o', 'media=a4', '-o', 'scaling=100', '-n', str(int(copies)), filename])
        return success
    else:
        return True

def get_day():
    return time.strftime('%a', time.localtime())

def get_year():
    return time.strftime('%Y', time.localtime())
