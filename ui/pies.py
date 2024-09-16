import bpy
from bpy.types import Menu

from .. utils.icons import get_icon, register_icons, unregister_icons


class CustomPropertyGroup(bpy.types.PropertyGroup):
	subd_levels: bpy.props.IntProperty(name='Levels', soft_min=0, soft_max=10)
	subd_vis: bpy.props.BoolProperty(name='Vis')

	mirror_vis: bpy.props.BoolProperty(name='Vis')
	
	string_field: bpy.props.StringProperty(name='string field')
	float_slider: bpy.props.FloatProperty(name='float value', soft_min=0, soft_max=10)


class PieSave(Menu):
	bl_idname = "MACHIN3_MT_save_pie"
	bl_label = "Save, Open, Append"

	def draw(self, context):
		layout = self.layout
		pie = layout.menu_pie()

		# 4 - LEFT
		pie.operator("wm.open_mainfile", text="Open...", icon_value=get_icon('open'))

		# 6 - RIGHT
		pie.operator("machin3.save", text="Save", icon_value=get_icon('save'))

		# 2 - BOTTOM
		pie.operator("wm.save_as_mainfile", text="Save As..", icon_value=get_icon('save_as'))

		# 8 - TOP
		box = pie.split()
		# box = pie.box().split()

		b = box.box()
		column = b.column()
		self.draw_left_column(column)

		column = box.column()
		b = column.box()
		self.draw_center_column_top(b)

		#if bpy.data.filepath:
		#	b = column.box()
		#	self.draw_center_column_bottom(b)

		b = box.box()
		column = b.column()
		self.draw_right_column(column)

		# 7 - TOP - LEFT
		pie.separator()

		# 9 - TOP - RIGHT
		pie.separator()

		# 1 - BOTTOM - LEFT
		pie.operator("machin3.new", text="New", icon_value=get_icon('new'))

		# 3 - BOTTOM - RIGHT
		pie.operator("machin3.save_incremental", text="Incremental Save", icon_value=get_icon('save_incremental'))

	def draw_left_column(self, col):
		col.scale_x = 1.1

		row = col.row()
		row.scale_y = 1.5
		#row.operator("machin3.load_most_recent", text="(R) Most Recent", icon_value=get_icon('open_recent'))
		# row.operator("wm.call_menu", text="All Recent", icon_value=get_icon('open_recent')).name = "INFO_MT_file_open_recent"
		row.operator("wm.call_menu", text="All Recent", icon_value=get_icon('open_recent')).name = "TOPBAR_MT_file_open_recent"

		col.separator()
		col.operator("wm.recover_auto_save", text="Recover Auto Save...", icon_value=get_icon('recover_auto_save'))
		# col.operator("wm.recover_last_session", text="Recover Last Session", icon='RECOVER_LAST')
		col.operator("wm.revert_mainfile", text="Revert", icon_value=get_icon('revert'))

	def draw_center_column_top(self, col):
		row = col.split(factor=0.25)
		row.label(text="OBJ")
		r = row.row(align=True)
		r.operator("import_scene.obj", text="Import", icon_value=get_icon('import'))
		r.operator("export_scene.obj", text="Export", icon_value=get_icon('export'))

		row = col.split(factor=0.25)
		row.label(text="FBX")
		r = row.row(align=True)
		r.operator("import_scene.fbx", text="Import", icon_value=get_icon('import'))
		r.operator("export_scene.fbx", text="Export", icon_value=get_icon('export'))

	def draw_center_column_bottom(self, col):
		#row = col.split(factor=0.5)
		#row.scale_y = 1.25
		#row.operator("machin3.load_previous", text="Previous", icon_value=get_icon('open_previous'))
		#row.operator("machin3.load_next", text="Next", icon_value=get_icon('open_next'))
		pass

	def draw_right_column(self, col):
		row = col.row()
		r = row.row(align=True)
		r.operator("wm.append", text="Append", icon_value=get_icon('append'))
		r.operator("wm.link", text="Link", icon_value=get_icon('link'))
		row.operator("wm.call_menu", text="", icon_value=get_icon('external_data')).name = "TOPBAR_MT_file_external_data"

		# append world and materials

		#appendworldpath = get_prefs().appendworldpath
		#appendmatspath = get_prefs().appendmatspath
		appendworldpath = ""
		appendmatspath = ""

		#if any([appendworldpath, appendmatspath]):
		#	col.separator()

		#	if appendworldpath:
		#		row = col.split(factor=0.8)
		#		row.scale_y = 1.5
				#row.operator("machin3.append_world", text="World", icon_value=get_icon('world'))
				#row.operator("machin3.load_world_source", text="", icon_value=get_icon('open_world'))

		#	if appendmatspath:
		#		row = col.split(factor=0.8)
		#		row.scale_y = 1.5
				#row.operator("wm.call_menu", text="Material", icon_value=get_icon('material')).name = "MACHIN3_MT_append_materials"
				#row.operator("machin3.load_materials_source", text="", icon_value=get_icon('open_material'))


class WAZOU_PIE_Apply_Transforms(Menu):
	bl_label = "Wazou Apply Transforms"
	bl_idname = "WAZOU_MT_apply_transforms"

	def draw(self, context):
		layout = self.layout
		pie = layout.menu_pie()
		#4 - LEFT
		pie.operator("wazou_transforms.apply_clear", text="Clear All", icon='EMPTY_AXIS').apply_clear = 'clear_all'
		#6 - RIGHT
		pie.operator("wazou_transforms.apply_clear", text="Apply Scale", icon='FILE_TICK').apply_clear = 'apply_scale'
		#2 - BOTTOM
		pie.operator("wazou_transforms.apply_clear", text="Apply Rot/Sca",
					 icon='FILE_TICK').apply_clear = 'apply_rot_scale'
		#8 - TOP
		pie.operator("wazou_transforms.apply_clear", text="Apply Location",
					 icon='FILE_TICK').apply_clear = 'apply_location'

		#7 - TOP - LEFT
		pie.operator("wazou_transforms.apply_clear", text="Apply All", icon='FILE_TICK').apply_clear = 'apply_all'
		#9 - TOP - RIGHT
		pie.operator("wazou_transforms.apply_clear", text="Apply Rotation",
					 icon='FILE_TICK').apply_clear = 'apply_rotation'

		#1 - BOTTOM - LEFT
		split = pie.split()
		col = split.column(align=True)
		row = col.row(align=True)
		row.separator()
		row = col.row(align=True)
		row.separator()
		row = col.row(align=True)
		row.separator()
		row = col.row(align=True)
		row.separator()
		row = col.row(align=True)
		row.separator()
		row = col.row(align=True)
		row.separator()
		row = col.row(align=True)
		row.scale_y = 1.3
		row.operator("object.location_clear", text="Clear Location", icon='EMPTY_AXIS')
		row = col.row(align=True)
		row.scale_y = 1.3
		row.operator("object.rotation_clear", text="Clear Rotation", icon='EMPTY_AXIS')
		row = col.row(align=True)
		row.scale_y = 1.3
		row.operator("object.scale_clear", text="Clear Scale", icon='EMPTY_AXIS')
		row = col.row(align=True)
		row.scale_y = 1.3
		row.operator("object.origin_clear", text="Clear Origin", icon='EMPTY_AXIS')

		#3 - BOTTOM - RIGHT
		split = pie.split()
		col = split.column(align=True)
		row = col.row(align=True)
		row.scale_y = 1.3
		row.operator("object.visual_transform_apply", text="Apply Visual Transforms", icon='FILE_TICK')
		row = col.row(align=True)
		row.scale_y = 1.3
		row.operator("object.duplicates_make_real", text="Make Duplicates Real", icon='USER')



class WAZOU_Pie_Origin_Pivot(Menu):
	bl_label = "Wazou Origin Pivot"
	bl_idname = "WAZOU_MT_origin_pivot"

	def draw(self, context):
		layout = self.layout
		pie = layout.menu_pie()
		# 4 - LEFT
		pie.operator("object.origin_set", text="Origin To 3D Cursor", icon='PIVOT_CURSOR').type = 'ORIGIN_CURSOR'
		# 6 - RIGHT
		pie.operator("view3d.snap_cursor_to_selected", text="Cursor to Selected", icon='PIVOT_CURSOR')
		# 2 - BOTTOM
		split = pie.split()
		col = split.column(align=True)
		row = col.row(align=True)
		row.scale_y = 1.3
		row.operator("view3d.snap_selected_to_grid", text="Sel to Grid", icon='RESTRICT_SELECT_OFF')
		row = col.row(align=True)
		row.scale_y = 1.3
		row.operator("view3d.snap_selected_to_cursor", text="Sel to Cursor (O)",icon='RESTRICT_SELECT_OFF').use_offset = True
		# 8 - TOP
		pie.operator("wazou_pivot.to_selection", text="Origin To Selection", icon='PIVOT_BOUNDBOX')
		# 7 - TOP - LEFT
		pie.operator("object.origin_set", text="Origin To Geometry", icon='PIVOT_BOUNDBOX').type = 'ORIGIN_GEOMETRY'
		# 9 - TOP - RIGHT
		pie.operator("view3d.snap_selected_to_cursor", text="Selection to Cursor", icon='RESTRICT_SELECT_OFF').use_offset = False
		# 1 - BOTTOM - LEFT
		split = pie.split()
		col = split.column(align=True)
		row = col.row(align=True)
		row.scale_y = 1.3
		row.operator("wazou_pivo.to_bottom", text="O to Bottom", icon='PIVOT_BOUNDBOX')
		row = col.row(align=True)
		row.scale_y = 1.3
		row.operator("object.origin_set", text="O to Center of Mass", icon='PIVOT_BOUNDBOX').type = 'ORIGIN_CENTER_OF_MASS'
		row = col.row(align=True)
		row.scale_y = 1.3
		row.operator("object.origin_set", text="Geometry To O", icon='PIVOT_BOUNDBOX').type = 'GEOMETRY_ORIGIN'
		
		# 3 - BOTTOM - RIGHT
		split = pie.split()
		col = split.column(align=True)

		row = col.row(align=True)
		row.scale_y = 1.3
		row.operator("view3d.snap_cursor_to_center", text="Cursor to Center", icon='PIVOT_CURSOR')
		row = col.row(align=True)
		row.scale_y = 1.3
		row.operator("view3d.snap_cursor_to_active", text="Cursor to Active", icon='PIVOT_CURSOR')
		row = col.row(align=True)
		row.scale_y = 1.3
		row.operator("view3d.snap_cursor_to_grid", text="Cursor to Grid", icon='PIVOT_CURSOR')


class PIE_MT_PieDelete(Menu):
	bl_idname = "PIE_MT_delete"
	bl_label = "Pie Delete"

	def draw(self, context):
		layout = self.layout
		pie = layout.menu_pie()
		# 4 - LEFT
		box = pie.split().column()
		box.operator("mesh.dissolve_limited", text="Limited Dissolve", icon='STICKY_UVS_LOC')
		box.operator("mesh.delete_edgeloop", text="Delete Edge Loops", icon='NONE')
		box.operator("mesh.edge_collapse", text="Edge Collapse", icon='UV_EDGESEL')
		# 6 - RIGHT
		box = pie.split().column()
		box.operator("mesh.remove_doubles", text="Merge By Distance", icon='NONE')
		box.operator("mesh.delete", text="Only Edge & Faces", icon='NONE').type = 'EDGE_FACE'
		box.operator("mesh.delete", text="Only Faces", icon='UV_FACESEL').type = 'ONLY_FACE'
		# 2 - BOTTOM
		pie.operator("mesh.dissolve_edges", text="Dissolve Edges", icon='SNAP_EDGE')
		# 8 - TOP
		pie.operator("mesh.delete", text="Delete Edges", icon='EDGESEL').type = 'EDGE'
		# 7 - TOP - LEFT
		pie.operator("mesh.delete", text="Delete Vertices", icon='VERTEXSEL').type = 'VERT'
		# 9 - TOP - RIGHT
		pie.operator("mesh.delete", text="Delete Faces", icon='FACESEL').type = 'FACE'
		# 1 - BOTTOM - LEFT
		pie.operator("mesh.dissolve_verts", text="Dissolve Vertices", icon='SNAP_VERTEX')
		# 3 - BOTTOM - RIGHT
		pie.operator("mesh.dissolve_faces", text="Dissolve Faces", icon='SNAP_FACE')


class PIE_MT_SelectionsMore(Menu):
	bl_idname = "PIE_MT_selectionsmore"
	bl_label = "Pie Selections Object Mode"

	def draw(self, context):
		layout = self.layout
		pie = layout.menu_pie()
		box = pie.split().column()
		box.operator("object.select_random", text="Select Random")
		box.operator("object.select_linked", text="Select Linked")
		box.separator()

		box.operator("object.select_more", text="More")
		box.operator("object.select_less", text="Less")
		box.separator()

		props = box.operator("object.select_hierarchy", text="Parent")
		props.extend = False
		props.direction = 'PARENT'

		props = box.operator("object.select_hierarchy", text="Child")
		props.extend = False
		props.direction = 'CHILD'
		box.separator()

		props = box.operator("object.select_hierarchy", text="Extend Parent")
		props.extend = True
		props.direction = 'PARENT'

		props = box.operator("object.select_hierarchy", text="Extend Child")
		props.extend = True
		props.direction = 'CHILD'


class PIE_MT_ObjectLink(Menu):
	bl_idname = "PIE_MT_ObjectLink"
	bl_label = "Pie Object Link"

	def draw(self, context):
		layout = self.layout
		pie = layout.menu_pie()
		box = pie.split().column()

		#box.separator()
		box.operator("object.select_linked", text="Object data").type = "OBDATA"
		box.operator("object.select_linked", text="Materials").type = "MATERIAL"
		box.operator("object.select_linked", text="Instanced collection").type = "DUPGROUP"
		box.operator("object.select_linked", text="Particles").type = "PARTICLE"
		box.operator("object.select_linked", text="Library ").type = "LIBRARY"
		box.operator("object.select_linked", text="Library object data").type = "LIBRARY_OBDATA"

		
class PIE_MT_AKM_Link(Menu):
	bl_idname = "PIE_MT_akm_link"
	bl_label = "AKM Link"

	def draw(self, context):
		layout = self.layout
		pie = layout.menu_pie()
		
		#1 - LEFT
		pie.separator()

		#2 - RIGHT
		# ------------------------------------------------------------
		# Select
		# ------------------------------------------------------------
		split = pie.split()
		col = split.column(align=False)
		col.scale_x = 2
		col = split.column(align=False)
		col.scale_x = 3
		box = col.box()
		row = box.row(align=True)
		row.menu("PIE_MT_selectionsmore", text="Select Menu")
		# pie.menu("PIE_MT_selectionsmore", text="Select Menu")
		#pie.menu("PIE_MT_ObjectLink", text="Select linked")

		#3 - BOTTOM
		# ------------------------------------------------------------
		# Select linked
		# ------------------------------------------------------------
		split = pie.split()
		box = split.column(align=True)
		box_l = box.box()
		row = box_l.row(align=True)
		row.label(text="Select linked", icon = "UV_SYNC_SELECT")
		# box_l.separator()
		row = box_l.row(align=True)

		# Object data
		row.operator("object.select_linked", text="OD", icon = "OBJECT_DATA").type = "OBDATA"
		row.separator()
		# Materials
		row.operator("object.select_linked", text="MAT", icon = "MATERIAL").type = "MATERIAL"
		row.separator()
		# Instanced collection
		row.operator("object.select_linked", text="INST COL", icon = "OUTLINER_OB_GROUP_INSTANCE").type = "DUPGROUP"
		row.separator()
		# Particles
		row.operator("object.select_linked", text="PRT", icon = "PARTICLE_DATA").type = "PARTICLE"
		row.separator()
		# Library
		row.operator("object.select_linked", text="LIB", icon = "DUPLICATE").type = "LIBRARY"
		row.separator()
		# Library object data
		row.operator("object.select_linked", text="LIB OD", icon = "MOD_DATA_TRANSFER").type = "LIBRARY_OBDATA"

		box.separator()

		box_l = box.box()
		row = box_l.row(align=True)
		row.label(text="Copy", icon = "COPYDOWN")
		# box_l.separator()
		row = box_l.row(align=True)
		
		row.operator("object.make_links_data", text="Modifiers").type = "MODIFIERS"
		row.separator()
		row.operator("object.make_links_data", text="Grease pencil effects").type = "EFFECTS"

		#4 - TOP
		# ------------------------------------------------------------
		# Link transfer
		# ------------------------------------------------------------
		split = pie.split()
		box = split.column(align=True)
		box_l = box.box()
		row = box_l.row(align=True)
		row.label(text="Link transfer", icon='LINKED')
		# box.separator()
		row = box_l.row(align=True)
		#Object data
		row.operator("object.make_links_data", text="OD", icon = "OBJECT_DATA").type = "OBDATA"
		row.separator()
		# Materials
		row.operator("object.make_links_data", text="MAT", icon = "MATERIAL").type = "MATERIAL"
		row.separator()
		# Animation
		row.operator("object.make_links_data", text="ANM", icon = "DECORATE_ANIMATE").type = "ANIMATION"
		row.separator()
		# Collections
		row.operator("object.make_links_data", text="GRP", icon = "OUTLINER_COLLECTION").type = "GROUPS"
		row.separator()
		# Instance Collection
		row.operator("object.make_links_data", text="GRP INST", icon = "OUTLINER_OB_GROUP_INSTANCE").type = "DUPLICOLLECTION"
		row.separator()
		# Fonts to text
		row.operator("object.make_links_data", text="FNT", icon= "FONT_DATA").type = "FONTS"
		box.separator()
	
		#4 - TOP-LEFT
		split = pie.split()
		col = split.column(align=False)
		col.scale_x = 2
		box = col.box()
		row = box.row(align=True)
		row.label(text="User", icon='USER')
		row = box.row(align=True)
		row.operator("object.make_single_user", text="Make single user")

		box = col.box()
		row = box.row(align=True)
		row.label(text="Link collection", icon='OUTLINER_COLLECTION')
		row = box.row(align=True)
		row.operator("akm_menus.move_selected_to_active_collection", text="Move selected to collection")

		col = split.column(align=False)
		col.scale_x = 3
	
		#5 - TOP-RIGHT
		pie.separator()

		#6 - BOTTOM-LEFT
		pie.separator()

		#7 - BOTTOM-RIGHT
		pie.separator()


class PIE_MT_PieNormals(Menu):
	bl_idname = "PIE_MT_normals"
	bl_label = "Pie Normals"
	# Меню нормалей
	# Выделить объекты с залоченными нормалями
	# +++ Убрать залоченные нормали
	# Стандартные операции с нормалями.
	# Настройки показа нормалей
	# выбрать хард софт эджи

	def draw(self, context):
		layout = self.layout
		pie = layout.menu_pie()
		# 4 - LEFT
		box = pie.split().column()
		box.operator("mesh.flip_normals", text="Flip")
		box.operator("mesh.normals_make_consistent", text="Recalculate Outside").inside = False
		box.operator("mesh.normals_make_consistent", text="Recalculate Inside").inside = True
		# 6 - RIGHT
		box = pie.split().column()
		
		if context.mode == "OBJECT":
			box.operator("akm_menus.clear_split_normals", text="Clear split normals", icon='NONE')
			box.operator("akm_menus.set_smooth_180", text="Set smooth (180)")
			box.operator("object.shade_flat")
			box.operator("object.shade_smooth")
			box.operator("object.shade_smooth", text="Set autosmooth").use_auto_smooth=True

		if context.mode == "EDIT_MESH":
			box.operator("mesh.faces_shade_smooth", text="Smooth Faces")
			box.operator("mesh.faces_shade_flat", text="Flat Faces")
			box.operator("mesh.mark_sharp", text="Smooth Edges").clear = True
			box.operator("mesh.mark_sharp", text="Sharp Edges")
			props = box.operator("mesh.mark_sharp", text="Smooth Vertices")
			props.use_verts = True
			props.clear = True
			box.operator("mesh.mark_sharp", text="Sharp Vertices").use_verts = True
		
		# 2 - BOTTOM
		
		# 8 - TOP
		
		# 7 - TOP - LEFT
		
		# 9 - TOP - RIGHT
		
		# 1 - BOTTOM - LEFT
		
		# 3 - BOTTOM - RIGHT
		


class PIE_MT_AKM_Modifiers(Menu):
	bl_idname = "PIE_MT_akm_modifiers"
	bl_label = "AKM Modifiers"

	# TODO выделение объектов с модификатором

	def draw(self, context):
		layout = self.layout
		pie = layout.menu_pie()
		
		#1 - LEFT
		pie.separator()

		#2 - RIGHT
		pie.separator()

		#3 - BOTTOM
		group = pie.column()
		box_l = group.box()
		box_l.label(text="Delete/Collapse")
		col = box_l.column(align=True)
		col.operator("akm_menus.collapse_modifiers", text="Collapse modifiers")
		col.operator("akm_menus.remove_modifiers", text="Remove modifiers")
		col.operator("akm_menus.remove_subd_modifiers", text="Remove subd modifiers")
		row = box_l.row().box()
		row.operator("akm_menus.collapse_modifiers", text="1111")
		row.operator("akm_menus.collapse_modifiers", text="2222")
		
		row = box_l.split(align=True, factor=0.2)
		row.operator("akm_menus.collapse_modifiers", text="1111")
		row.operator("akm_menus.collapse_modifiers", text="2222")

		#4 - TOP
		# TODO вынести видимость настроек по типам модификаторов в преференсы аддона
		group = pie.column()
		box_l = group.box()
		box_l.label(text="Subdivision", icon="MOD_SUBSURF")
		row = box_l.row(align=True)
		row.operator("akm_menus.set_visibility_subd_modifier", text="Set subd modifier visibile").show = bpy.context.scene.custom_props.subd_vis
		row.separator()
		row.prop(bpy.context.scene.custom_props, "subd_vis")
		row = box_l.row(align=True)
		row.operator("akm_menus.set_subd_modifier_levels", text="Set subd levels").levels = bpy.context.scene.custom_props.subd_levels
		row.separator_spacer()
		row.separator()
		row.prop(bpy.context.scene.custom_props, "subd_levels")
		group.separator()

		box_l = group.box()
		box_l.label(text="Mirror", icon="MOD_MIRROR")
		row = box_l.row(align=True)
		row.operator("akm_menus.set_visibility_mirror_modifier", text="Set mirror modifier visible").show = bpy.context.scene.custom_props.mirror_vis
		row.separator()
		row.prop(bpy.context.scene.custom_props, "mirror_vis")
	
		#5 - TOP-LEFT
		pie.separator()

		#6 - TOP-RIGHT
		pie.separator()

		#7 - BOTTOM-LEFT
		pie.separator()

		#8 - BOTTOM-RIGHT
		pie.separator()


class PIE_MT_PieTest(Menu):
	bl_idname = "PIE_MT_Test"
	bl_label = "Pie Test"

	# subd_levels : bpy.props.IntProperty(default=0)

	def draw(self, context):
		layout = self.layout
		pie = layout.menu_pie()

		#1 - LEFT
		pie.separator()

		#2 - RIGHT
		box = pie.split().column()
		box_l = box.box()
		box_l.operator("akm_menus.delete_all_uvs", text="Delete all uvs")

		#3 - SOUTH
		box = pie.split().column()

		box.operator("wazou_rmb_pie_menus.test", text="Test")
		box.operator("object.modal_operator", text="Test modal")
		box.operator("view3d.modal_operator_raycast", text="Test raycast")
		box.separator()

		box_l = box.box()
		box_l.operator("akm_menus.delete_all_uvs", text="Delete all uvs")
		box_l.operator("akm_menus.set_smooth_180", text="Set smooth (180)")
		box_l.operator("akm_menus.delete_all_mats", text="Delete all mats")
		box_l.separator()
		# box_l.operator("akm_menus.move_selected_to_active_collection", text="Move sel to collection")
		# box_l.separator()
		box_l.operator("akm_menus.clear_split_normals", text="Clear custom split normals")

		

		#4 - TOP
		pie.separator()
	

		#5 - TOP-LEFT
		split = pie.split()
		col = split.column(align=False)
		box_l = col.box()
		row = box_l.row(align=False)
		row.scale_x = 2
		row.label(text="User", icon='USER')
		row = box_l.row(align=False)
		row.operator("object.make_single_user", text="Make single user")
		
		# box.separator()

		# box_l = box.box()
		# row = box_l.row(align=True)
		# row.label(text="Link collection", icon='OUTLINER_COLLECTION')
		# row = box_l.row(align=True)
		# row.operator("akm_menus.move_selected_to_active_collection", text="Move selected to collection")

		# split = pie.split()
		# col = split.column(align=True)
		# col.operator("akm_menus.delete_all_uvs", text="Delete all uvs")
		# col = split.column(align=True)
		# col.operator("akm_menus.delete_all_uvs", text="Delete all uvs")
		# col = split.column(align=True)
		# col = split.column(align=True)
		# col = split.column(align=True)
		

		#6 - TOP-RIGHT
		pie.separator()

		#6 - BOTTOM-LEFT
		pie.separator()

		#7 - BOTTOM-RIGHT
		pie.separator()

		

		


classes = (
	CustomPropertyGroup,
	PieSave,
	WAZOU_Pie_Origin_Pivot,
	WAZOU_PIE_Apply_Transforms,
	PIE_MT_PieDelete,
	PIE_MT_AKM_Link,
	PIE_MT_PieNormals,
	PIE_MT_AKM_Modifiers,
	PIE_MT_SelectionsMore,
	PIE_MT_ObjectLink,
	PIE_MT_PieTest,
	)

def register():
	register_icons()

	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.Scene.custom_props = bpy.props.PointerProperty(type=CustomPropertyGroup)


def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)

	del bpy.types.Scene.custom_props
	

	unregister_icons()
	