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

from . import auto_load

from .ui import pies
from .operators import simple_modal_operator
from .operators import operators

bl_info = {
	"name": "AutoHotkeys",
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

addon_keymaps = []

def register_keymaps():
	global addon_keymaps

	wm = bpy.context.window_manager
	kc = wm.keyconfigs.addon
	if kc:
		# ------------------------------------------------------------------------------------------
		# Pies.
		# ------------------------------------------------------------------------------------------

		# Object mode.

		# TODO меню переключения видов, орфографическая, камера, шейдинг и некоторые настройки вьюпорта

		km = kc.keymaps.new(name="Object Mode")

		# Save, load, append ...
		kmi = km.keymap_items.new(idname="wm.call_menu_pie", type="S", value="PRESS")
		kmi.ctrl = True
		kmi.properties.name = pies.PieSave.bl_idname
		addon_keymaps.append((km, kmi))

		# Origin, pivot
		kmi = km.keymap_items.new(idname="wm.call_menu_pie", type="C", value="PRESS")
		kmi.shift = True
		kmi.properties.name = pies.WAZOU_Pie_Origin_Pivot.bl_idname
		addon_keymaps.append((km, kmi))

		# Transforms
		kmi = km.keymap_items.new(idname="wm.call_menu_pie", type="A", value="PRESS")
		kmi.ctrl = True
		kmi.properties.name = pies.WAZOU_PIE_Apply_Transforms.bl_idname
		addon_keymaps.append((km, kmi))

		# Link
		# TODO Выделение обжект дата с добавление по шифту (объекты добавляются к выделению уже существующему).
		kmi = km.keymap_items.new(idname="wm.call_menu_pie", type="L", value="PRESS")
		kmi.properties.name = pies.PIE_MT_AKM_Link.bl_idname
		addon_keymaps.append((km, kmi))

		kmi = km.keymap_items.new(idname="wm.call_menu_pie", type="T", value="PRESS")
		kmi.alt = True
		kmi.properties.name = pies.PIE_MT_AKM_Modifiers.bl_idname
		addon_keymaps.append((km, kmi))
		
		# Test
		kmi = km.keymap_items.new('wm.call_menu_pie', 'F3', 'PRESS')
		kmi.properties.name = pies.PIE_MT_PieTest.bl_idname
		kmi.alt = True
		addon_keymaps.append((km, kmi))

		# Mesh mode.

		km = kc.keymaps.new(name="Mesh")

		# Origin, pivot
		kmi = km.keymap_items.new(idname="wm.call_menu_pie", type="C", value="PRESS")
		kmi.shift = True
		kmi.properties.name = pies.WAZOU_Pie_Origin_Pivot.bl_idname
		addon_keymaps.append((km, kmi))

		# Delete
		#km = wm.keyconfigs.addon.keymaps.new(name='Mesh')
		kmi = km.keymap_items.new('wm.call_menu_pie', 'X', 'PRESS')
		kmi.properties.name = "PIE_MT_delete"
		addon_keymaps.append((km, kmi))


		# ------------------------------------------------------------------------------------------
		# Hotkeys.
		# ------------------------------------------------------------------------------------------

		# Object mode.

		#km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
		km = kc.keymaps.new(name="Object Mode")

		# Transform
		#kmi = km.keymap_items.new(idname="transform.resize", type="R", value="PRESS")
		#addon_keymaps.append((km, kmi))

		#kmi = km.keymap_items.new(idname="wm.tool_set_by_id", type="R", value="PRESS")
		#kmi.alt = True
		#setattr(kmi.properties, "name", "builtin.scale")
		#addon_keymaps.append((km, kmi))

		kmi = km.keymap_items.new(idname="object.modal_operator", type="F4", value="PRESS")
		kmi.shift = True
		addon_keymaps.append((km, kmi))

		# Delete.
		kmi = km.keymap_items.new(idname="object.delete", type="X", value="PRESS")
		setattr(kmi.properties, "confirm", True)
		addon_keymaps.append((km, kmi))

		# Select
		kmi = km.keymap_items.new(idname="view3d.select_circle", type="C", value="PRESS")
		kmi.alt = True
		addon_keymaps.append((km, kmi))

		# Link
		# kmi = km.keymap_items.new(idname="wm.call_menu", type="L", value="PRESS", any=False, shift=False, ctrl=True, alt=False, oskey=False, key_modifier='NONE', direction='ANY', repeat=True, head=False)
		# kmi.properties.name = "VIEW3D_MT_make_links"
		# addon_keymaps.append((km, kmi))

		# kmi = km.keymap_items.new(idname="object.select_linked", type="L", value="PRESS", any=False, shift=True, ctrl=False, alt=False, oskey=False, key_modifier='NONE', direction='ANY', repeat=True, head=False)

		# # User data
		# kmi = km.keymap_items.new(idname="object.make_single_user", type="L", value="PRESS")
		# kmi.alt = True
		# addon_keymaps.append((km, kmi))

		# Mesh

		# TODO extrude.
		# TODO slide vertex edge посмотртеть как в питоне конфига задаётся слайд модификатор для мува.
		# TODO меню для select grouped bpy.ops.object.select_grouped(type='CHILDREN_RECURSIVE')
		# TODO вделать на shift + S  пуш\пулл, на alt + S сринк\флаттен

		km = kc.keymaps.new(name="Mesh")

		# Save
		kmi = km.keymap_items.new(idname="wm.call_menu_pie", type="S", value="PRESS")
		kmi.ctrl = True
		kmi.properties.name = pies.PieSave.bl_idname
		addon_keymaps.append((km, kmi))

		# Transform
		#kmi = km.keymap_items.new(idname="transform.resize", type="R", value="PRESS")
		#addon_keymaps.append((km, kmi))

		#kmi = km.keymap_items.new(idname="wm.tool_set_by_id", type="R", value="PRESS")
		#kmi.alt = True
		#setattr(kmi.properties, "name", "builtin.scale")
		#addon_keymaps.append((km, kmi))

		# Slide
		#kmi = km.keymap_items.new(idname="transform.vert_slide", type="NUMPAD_1", value="PRESS")
		#kmi.alt = True
		#addon_keymaps.append((km, kmi))

		# Link
		kmi = km.keymap_items.new(idname="mesh.select_linked_pick", type="L", value="PRESS")
		setattr(kmi.properties, "deselect", False)
		addon_keymaps.append((km, kmi))

		kmi = km.keymap_items.new(idname="mesh.select_linked_pick", type="L", value="PRESS")
		kmi.shift = True
		setattr(kmi.properties, "deselect", True)
		addon_keymaps.append((km, kmi))


		# Select
		kmi = km.keymap_items.new(idname="view3d.select_circle", type="C", value="PRESS")
		kmi.alt = True
		addon_keymaps.append((km, kmi))


		# Knife
		kmi = km.keymap_items.new(idname="wm.tool_set_by_id", type="K", value="PRESS")
		kmi.alt = True
		setattr(kmi.properties, "name", "builtin.knife")
		setattr(kmi.properties, "cycle", True)
		addon_keymaps.append((km, kmi))

		kmi = km.keymap_items.new(idname="mesh.knife_tool", type="K", value="PRESS")
		setattr(kmi.properties, "use_occlude_geometry", True)
		addon_keymaps.append((km, kmi))

		# Loop cut
		kmi = km.keymap_items.new(idname="mesh.loopcut_slide", type="K", value="PRESS")
		kmi.shift = True
		#setattr(kmi.properties, "name", "builtin.knife")
		addon_keymaps.append((km, kmi))

		# Connect
		kmi = km.keymap_items.new(idname="mesh.vert_connect_path", type="J", value="PRESS")
		addon_keymaps.append((km, kmi))


		# Split, separate, rip
		kmi = km.keymap_items.new(idname="mesh.separate", type="V", value="PRESS")
		kmi.alt = True
		addon_keymaps.append((km, kmi))

		kmi = km.keymap_items.new(idname="mesh.split", type="V", value="PRESS")
		kmi.ctrl = True
		addon_keymaps.append((km, kmi))

		kmi = km.keymap_items.new(idname="mesh.rip_move", type="V", value="PRESS")
		kmi.shift = True
		addon_keymaps.append((km, kmi))

		# Merge
		kmi = km.keymap_items.new(idname="mesh.merge", type="M", value="PRESS")
		kmi.alt = True
		addon_keymaps.append((km, kmi))

		# Connect path
		kmi = km.keymap_items.new(idname="mesh.vert_connect_path", type="M", value="PRESS")
		addon_keymaps.append((km, kmi))

def unregister_keymaps():
	global addon_keymaps

	for km, kmi in addon_keymaps:
		km.keymap_items.remove(kmi)
	
	addon_keymaps.clear()


def register():
	register_addons()

	operators.register()
	pies.register()
	
	register_keymaps()

	#auto_load.register()


def unregister():
	unregister_addons()

	operators.unregister()
	pies.unregister()

	unregister_keymaps()

	#auto_load.unregister()

