import bpy

from . import pies

addon_keymaps = []

def register_hotkey(kc, mode, id, key, name):
	km = kc.keymaps.new(name=mode)

	kmi = km.keymap_items.new(idname=id, type=key, value="PRESS")
	# kmi.properties.name = name
	if (hasattr(kmi.properties, "name")):
		setattr(kmi.properties, "name", name)
	
	addon_keymaps.append((km, kmi))

	return kmi


def register_keymaps():
	global addon_keymaps

	wm = bpy.context.window_manager
	kc = wm.keyconfigs.addon
	if kc:
		# ------------------------------------------------------------------------------------------
		# Pies.
		# ------------------------------------------------------------------------------------------

		# TODO меню переключения видов, орфографическая, камера, шейдинг и некоторые настройки вьюпорта

		# Save, load, append ...
		kmi = register_hotkey(kc, "Object Mode", "wm.call_menu_pie", "S", pies.PieSave.bl_idname)
		kmi.ctrl = True

		# Origin, pivot
		kmi = register_hotkey(kc, "Object Mode",  "wm.call_menu_pie", "C", pies.WAZOU_Pie_Origin_Pivot.bl_idname)
		kmi.shift = True

		# Transforms
		kmi = register_hotkey(kc, "Object Mode",  "wm.call_menu_pie", "A", pies.WAZOU_PIE_Apply_Transforms.bl_idname)
		kmi.ctrl = True

		# Link
		# TODO Выделение обжект дата с добавление по шифту (объекты добавляются к выделению уже существующему).
		kmi = register_hotkey(kc, "Object Mode",  "wm.call_menu_pie", "L", pies.PIE_MT_AKM_Link.bl_idname)

		kmi = register_hotkey(kc, "Object Mode",  "wm.call_menu_pie", "T", pies.PIE_MT_AKM_Modifiers.bl_idname)
		kmi.alt = True
		
		# Test
		kmi = register_hotkey(kc, "Object Mode",  "wm.call_menu_pie", "F3", pies.PIE_MT_PieTest.bl_idname)
		kmi.alt = True


		# Origin, pivot
		kmi = register_hotkey(kc, "Mesh",  "wm.call_menu_pie", "C", pies.WAZOU_Pie_Origin_Pivot.bl_idname)
		kmi.shift = True

		# Delete
		kmi = register_hotkey(kc, "Mesh",  "wm.call_menu_pie", "X", "PIE_MT_delete")


		# ------------------------------------------------------------------------------------------
		# Hotkeys.
		# ------------------------------------------------------------------------------------------

		# Object mode.

		#km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
		# km = kc.keymaps.new(name="Object Mode")

		# Transform
		#kmi = km.keymap_items.new(idname="transform.resize", type="R", value="PRESS")
		#addon_keymaps.append((km, kmi))

		#kmi = km.keymap_items.new(idname="wm.tool_set_by_id", type="R", value="PRESS")
		#kmi.alt = True
		#setattr(kmi.properties, "name", "builtin.scale")
		#addon_keymaps.append((km, kmi))

		# kmi = km.keymap_items.new(idname="object.modal_operator", type="F4", value="PRESS")
		# kmi.shift = True
		# addon_keymaps.append((km, kmi))
		# kmi = register_hotkey(kc, "Object Mode", "object.modal_operator", "F4", "")
		# kmi.shift = True

		# Delete.
		kmi = register_hotkey(kc, "Object Mode", "object.delete", "X", "")
		setattr(kmi.properties, "confirm", True)

		# Select
		kmi = register_hotkey(kc, "Object Mode", "view3d.select_circle", "C", "")
		kmi.alt = True

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
