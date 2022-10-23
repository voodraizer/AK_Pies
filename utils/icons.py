import os

import bpy
from bpy.utils import previews

icons = None


def get_icon(name):
	global icons

	return icons[name].icon_id

def get_path():
	return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def get_name():
	return os.path.basename(get_path())

def get_prefs():
	return bpy.context.preferences.addons[get_name()].preferences


def register_icons():
	global icons
	
	path = os.path.join(get_path(), "icons")
	icons = previews.new()

	for i in sorted(os.listdir(path)):
		if i.endswith(".png"):
			iconname = i[:-4]
			filepath = os.path.join(path, i)

			icons.load(iconname, filepath, 'IMAGE')


def unregister_icons():
	global icons

	if (icons):
		previews.remove(icons)