# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


# TODO
# отключать клавиши с дупликатами
# выводить окошко с подсказками по установленным хоткеям
# визуальное редактирование хоткеев как в майа
# включать некоторые стандартные аддоны 
# менюшки как в майа на W + клик (правый клик), 1 + клик для вертексов ....
# завести репозиторий
# Назначение материала из списка.
# настройка криса эджей интеративно перетаскивая мышь
# настройка шарпа и юв эджей интеративно перетаскивая мышь в разные стороны
# интерактивное добавление миррора с указанием оси во вьюпорте. оси рисовать 
# миррор меша с флипом нормалей опционально.





import bpy

# from . import auto_load

from .ui import pies, hotkeys
from .operators import simple_modal_operator
from .operators import operators

bl_info = {
	"name": "AK Pie tools",
	"author": "vood",
	"description": "",
	"blender": (3, 3, 0),
	"version": (0, 0, 1),
	"location": "",
	"warning": "",
	"category": "User"
}


#auto_load.init()

addons = {"add_mesh_extra_objects", "add_curve_extra_objects", 
			"copy_global_transform", "space_view3d_pie_menus", 
			"mesh_tools", "mesh_looptools", 
			"space_view3d_copy_attributes"}

def register_addons():
	import bpy
	import addon_utils

	# TODO запоминать состояние адднонов в файл.

	global addons

	#for addon in bpy.context.preferences.addons:
	#	print(addon.module)

	for a in addons:
		#addon_utils.enable(a)
		#bpy.ops.preferences.addon_enable(module=a)
		#bpy.context.preferences.addon_enable(module=a)
		pass
	
	#bpy.ops.wm.save_userpref()
	
	pass

def unregister_addons():
	import bpy
	import addon_utils
	
	global addons

	for a in addons:
		#addon_utils.disable(a)
		#bpy.ops.preferences.addon_desable(module=a)
		pass
	
	#bpy.ops.wm.save_userpref()

	pass


def register():
	register_addons()

	operators.register()
	pies.register()
	
	hotkeys.register_keymaps()

	#auto_load.register()


def unregister():
	unregister_addons()

	operators.unregister()
	pies.unregister()

	hotkeys.unregister_keymaps()

	#auto_load.unregister()

