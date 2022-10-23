import bpy
import time

from bpy.props import (EnumProperty)

from . import simple_modal_operator




class WAZOU_RMB_PIE_MENUS_OT_test(bpy.types.Operator):
	"""    LOOPTOOLS BRIDGE/LOFT

	CLICK - 1 Segment Linear
	SHIFT - 2 Segments Cubic
	CTRL  - Parallel (All)
	ALT    - Cubic x5
	"""
	bl_idname = 'wazou_rmb_pie_menus.test'
	bl_label = "Looptools Bridge"
	bl_options = {'REGISTER'}


	def invoke(self, context, event):

		# if event.shift:
		# 	bpy.ops.mesh.looptools_bridge(True, cubic_strength=0, interpolation='cubic', loft=False, loft_loop=False,
		# 								  min_width=0, mode='shortest', remove_faces=True, reverse=False, segments=2,
		# 								  twist=0)

		# elif event.ctrl:
		# 	bpy.ops.mesh.looptools_bridge(True, cubic_strength=0, interpolation='cubic', loft=False, loft_loop=False,
		# 								  min_width=0, mode='shortest', remove_faces=True, reverse=False, segments=4,
		# 								  twist=0)

		# else:
		# 	bpy.ops.mesh.looptools_bridge(True, cubic_strength=0, interpolation='linear', loft=False, loft_loop=False,
		# 								  min_width=0, mode='shortest', remove_faces=True, reverse=False, segments=1,
		# 								  twist=0)

		# def execute(self, context):
		bpy.ops.object.duplicate()
		return bpy.ops.transform.translate('INVOKE_DEFAULT')

		# return {'FINISHED'}


def main_mod(context, event):
	from bpy_extras import view3d_utils
	"""Run this function on left mouse, execute the ray cast"""
	# get the context arguments
	scene = context.scene
	region = context.region
	rv3d = context.region_data
	coord = event.mouse_region_x, event.mouse_region_y

	# get the ray from the viewport and mouse
	view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
	ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

	ray_target = ray_origin + view_vector

	def visible_objects_and_duplis():
		"""Loop over (object, matrix) pairs (mesh only)"""

		depsgraph = context.evaluated_depsgraph_get()
		for dup in depsgraph.object_instances:
			if dup.is_instance:  # Real dupli instance
				obj = dup.instance_object
				yield (obj, dup.matrix_world.copy())
			else:  # Usual object
				obj = dup.object
				yield (obj, obj.matrix_world.copy())

	def obj_ray_cast(obj, matrix):
		"""Wrapper for ray casting that moves the ray into object space"""

		# get the ray relative to the object
		matrix_inv = matrix.inverted()
		ray_origin_obj = matrix_inv @ ray_origin
		ray_target_obj = matrix_inv @ ray_target
		ray_direction_obj = ray_target_obj - ray_origin_obj

		# cast the ray
		success, location, normal, face_index = obj.ray_cast(ray_origin_obj, ray_direction_obj)

		if success:
			return location, normal, face_index
		else:
			return None, None, None

	# cast rays and find the closest object
	best_length_squared = -1.0
	best_obj = None

	for obj, matrix in visible_objects_and_duplis():
		if obj.type == 'MESH':
			hit, normal, face_index = obj_ray_cast(obj, matrix)
			if hit is not None:
				hit_world = matrix @ hit
				scene.cursor.location = hit_world
				length_squared = (hit_world - ray_origin).length_squared
				if best_obj is None or length_squared < best_length_squared:
					best_length_squared = length_squared
					best_obj = obj

	# now we have the object under the mouse cursor,
	# we could do lots of stuff but for the example just select.
	if best_obj is not None:
		# for selection etc. we need the original object,
		# evaluated objects are not in viewlayer
		best_original = best_obj.original
		best_original.select_set(True)
		context.view_layer.objects.active = best_original

class ViewOperatorRayCast(bpy.types.Operator):
	"""Modal object selection with a ray cast"""
	bl_idname = "view3d.modal_operator_raycast"
	bl_label = "RayCast View Operator"

	def modal(self, context, event):
		if event.type in {'MIDDLEMOUSE', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
			# allow navigation
			return {'PASS_THROUGH'}
		elif event.type == 'LEFTMOUSE':
			main_mod(context, event)
			return {'RUNNING_MODAL'}
		elif event.type in {'RIGHTMOUSE', 'ESC'}:
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		if context.space_data.type == 'VIEW_3D':
			context.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}
		else:
			self.report({'WARNING'}, "Active space must be a View3d")
			return {'CANCELLED'}
		
class ModalOperator(bpy.types.Operator):
	"""Move an object with the mouse, example"""
	bl_idname = "object.modal_operator"
	bl_label = "Simple Modal Operator"

	first_mouse_x: bpy.props.IntProperty()
	first_value: bpy.props.FloatProperty()

	def modal(self, context, event):
		if event.type == 'MOUSEMOVE':
			delta = self.first_mouse_x - event.mouse_x
			context.object.location.x = self.first_value + delta * 0.01
			bpy.context.window.cursor_modal_set("HAND")
			bpy.context.window.cursor_set("HAND")

		elif event.type == 'LEFTMOUSE':
			return {'FINISHED'}

		elif event.type in {'RIGHTMOUSE', 'ESC'}:
			context.object.location.x = self.first_value
			bpy.context.window.cursor_modal_restore()
			bpy.context.window.cursor_modal_set("DEFAULT")
			bpy.context.window.cursor_set("DEFAULT")
			return {'CANCELLED'}

		return {'RUNNING_MODAL'}

	def invoke(self, context, event):
		if context.object:
			self.first_mouse_x = event.mouse_x
			self.first_value = context.object.location.x
			
			context.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}
		else:
			self.report({'WARNING'}, "No active object, could not finish")
			return {'CANCELLED'}


class AKM_MENUS_OT_delete_all_uvs(bpy.types.Operator):
	"""    Delete all uvs on selected objects"""

	bl_idname = 'akm_menus.delete_all_uvs'
	bl_label = "Delete all uvs"
	bl_options = {'REGISTER'}


	def invoke(self, context, event):
		selection = bpy.context.selected_objects

		for obj in selection:
			if obj.type != 'MESH': 
				continue
			
			layers = obj.data.uv_layers
			for uv_layer in reversed(layers):
				layers.remove(uv_layer)

		return {'FINISHED'}


class AKM_MENUS_OT_set_smooth_180(bpy.types.Operator):
	"""    Set smooth (180) on selected objects"""

	bl_idname = 'akm_menus.set_smooth_180'
	bl_label = "Set smooth 180"
	bl_options = {'REGISTER'}


	def invoke(self, context, event):
		selection = bpy.context.selected_objects
		active_obj = bpy.context.view_layer.objects.active

		for obj in selection:
			if obj.type != 'MESH': 
				continue
			
			bpy.context.view_layer.objects.active = obj
			bpy.ops.object.shade_smooth()

			# obj.data.use_auto_smooth = True
			obj.data.auto_smooth_angle = 3.14159
		
		bpy.context.view_layer.objects.active = active_obj

		return {'FINISHED'}


class AKM_MENUS_OT_delete_all_mats(bpy.types.Operator):
	"""    Delete all materials on selected objects"""

	bl_idname = 'akm_menus.delete_all_mats'
	bl_label = "Delete all materials"
	bl_options = {'REGISTER'}


	def invoke(self, context, event):
		selection = bpy.context.selected_objects
		active_obj = bpy.context.view_layer.objects.active

		for obj in selection:
			if obj.type != 'MESH': 
				continue
			
			bpy.context.view_layer.objects.active = obj
			
			for i in range(len(obj.material_slots)):
				obj.active_material_index = 0
				bpy.ops.object.material_slot_remove()
		
		bpy.context.view_layer.objects.active = active_obj

		return {'FINISHED'}


class AKM_MENUS_OT_move_selected_to_active_collection(bpy.types.Operator):
	"""    Move selected objects to active collection"""

	bl_idname = 'akm_menus.move_selected_to_active_collection'
	bl_label = "Move selected to active collection."
	bl_options = {'REGISTER'}


	def invoke(self, context, event):
		# active_col = bpy.context.view_layer.active_layer_collection.collection
		# coll_target = bpy.data.collections.get(active_col.name)
		# print("=================== " + active_col.name)

		active_obj = bpy.context.view_layer.objects.active
		coll_target = active_obj.users_collection[0]

		selection = bpy.context.selected_objects
		for obj in selection:
			if (active_obj == obj):
				continue
			
			# unlink object from old collection
			for old_coll in  obj.users_collection:
				old_coll.objects.unlink(obj)

			# link to new collection
			coll_target.objects.link(obj)

		return {'FINISHED'}


class AKM_MENUS_OT_set_visibility_subd_modifier(bpy.types.Operator):
	"""    Set visibility subdivision surface modifier on selected"""

	bl_idname = 'akm_menus.set_visibility_subd_modifier'
	bl_label = "Set visibility subdivision surface modifier on selected."
	bl_options = {'REGISTER'}

	show : bpy.props.BoolProperty(default=True)


	def invoke(self, context, event):
		selection = bpy.context.selected_objects
		for obj in selection:
			if obj.type != 'MESH': 
				continue
			
			mods = getattr(obj, "modifiers", [])
			for m in mods:
				if m.type == 'SUBSURF':
					# m.show_viewport ^= True
					m.show_viewport = self.show
		
		self.report({'INFO'}, "Set visibility")

		return {'FINISHED'}


class AKM_MENUS_OT_set_subd_modifier_levels(bpy.types.Operator):
	"""    Set subdivision surface modifier levels on selected"""

	bl_idname = 'akm_menus.set_subd_modifier_levels'
	bl_label = "Set subdivision surface modifier levels on selected."
	bl_options = {'REGISTER'}

	levels : bpy.props.IntProperty(default=0)


	def invoke(self, context, event):
		selection = bpy.context.selected_objects
		for obj in selection:
			if obj.type != 'MESH': 
				continue
			
			mods = getattr(obj, "modifiers", [])
			for m in mods:
				if m.type == 'SUBSURF':
					m.levels = self.levels
					m.render_levels = self.levels

		return {'FINISHED'}


class AKM_MENUS_OT_set_visibility_mirror_modifier(bpy.types.Operator):
	"""    Set visibility mirror modifier on selected"""

	bl_idname = 'akm_menus.set_visibility_mirror_modifier'
	bl_label = "Set visibility mirror modifier on selected."
	bl_options = {'REGISTER'}

	show : bpy.props.BoolProperty(default=True)


	def invoke(self, context, event):
		selection = bpy.context.selected_objects
		for obj in selection:
			if obj.type != 'MESH': 
				continue
			
			mods = getattr(obj, "modifiers", [])
			for m in mods:
				if m.type == 'MIRROR':
					m.show_viewport = self.show

		return {'FINISHED'}


class AKM_MENUS_OT_collapse_modifiers(bpy.types.Operator):
	"""    Collapse modifiers on selected"""

	bl_idname = 'akm_menus.collapse_modifiers'
	bl_label = "Collapse modifiers on selected."
	bl_options = {'REGISTER'}

	def invoke(self, context, event):
		selection = bpy.context.selected_objects
		for obj in selection:
			if obj.type != 'MESH': 
				continue
			
			mods = getattr(obj, "modifiers", [])
			for m in mods:
				if m.type == 'SUBSURF':
					# Skip subsurf modifiers
					continue
				# obj.modifiers.clear()
				# bpy.ops.object.convert(target='MESH')
				if not m.show_viewport:
					# Delete disabled modifiers
					bpy.ops.object.modifier_remove(modifier=m.name)	

				bpy.ops.object.modifier_apply(modifier=m.name)

		return {'FINISHED'}


class AKM_MENUS_OT_remove_modifiers(bpy.types.Operator):
	"""    Remove modifiers on selected"""

	bl_idname = 'akm_menus.remove_modifiers'
	bl_label = "Remove modifiers on selected."
	bl_options = {'REGISTER'}

	def invoke(self, context, event):
		selection = bpy.context.selected_objects
		for obj in selection:
			if obj.type != 'MESH': 
				continue
			
			mods = getattr(obj, "modifiers", [])
			for m in mods:
				bpy.ops.object.modifier_remove(modifier=m.name)	

		return {'FINISHED'}


class AKM_MENUS_OT_remove_subd_modifiers(bpy.types.Operator):
	"""    Remove subd modifiers on selected"""
	
	bl_idname = 'akm_menus.remove_subd_modifiers'
	bl_label = "Remove subd modifiers on selected."
	bl_options = {'REGISTER'}

	def invoke(self, context, event):
		# TODO не работает на нескольких выделенных
		selection = bpy.context.selected_objects
		for obj in selection:
			if obj.type != 'MESH': 
				continue
			
			mods = getattr(obj, "modifiers", [])
			for m in mods:
				if m.type == 'SUBSURF':
					bpy.ops.object.modifier_remove(modifier=m.name)	

		return {'FINISHED'}


class AKM_MENUS_OT_splitnormals_clear(bpy.types.Operator):
	"""    Clear custom split normals on selected"""
	
	bl_idname = 'akm_menus.splitnormals_clear'
	bl_label = "Clear custom split normals."
	bl_options = {'REGISTER'}

	def invoke(self, context, event):
		selection = bpy.context.selected_objects
		for obj in selection:
			if obj.type != 'MESH': 
				continue
			
			bpy.ops.mesh.customdata_custom_splitnormals_clear()

		return {'FINISHED'}


class AKM_MENUS_OT_set_material_by_mouse_pos(bpy.types.Operator):
	"""    Set material"""
	# Назначение материала через пикер на полигоне объекта
	bl_idname = 'akm_menus.set_material_by_mouse_pos'
	bl_label = "Set material."
	bl_options = {'REGISTER'}

	def invoke(self, context, event):
		

		return {'FINISHED'}



class WAZOU_PIVOT_OT_align(bpy.types.Operator):
	bl_idname = "wazou_pivot.align"
	bl_label = "Use Pivot Align"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):

		if bpy.context.space_data.use_pivot_point_align == (False):
			bpy.context.space_data.use_pivot_point_align = True
		elif bpy.context.space_data.use_pivot_point_align == (True):
			bpy.context.space_data.use_pivot_point_align = False
		return {'FINISHED'}


# Pivot to selection
class WAZOU_PIVOT_OT_to_selection(bpy.types.Operator):
	bl_idname = "wazou_pivot.to_selection"
	bl_label = "Pivot To Selection"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		saved_location = bpy.context.scene.cursor.location.copy()
		bpy.ops.view3d.snap_cursor_to_selected()
		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
		bpy.context.scene.cursor.location = saved_location
		return {'FINISHED'}

# Pivot to Bottom
class WAZOU_PIVOT_OT_to_bottom(bpy.types.Operator):
	bl_idname = "wazou_pivo.to_bottom"
	bl_label = "Pivot To Bottom"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		mode = context.object.mode

		bpy.ops.object.mode_set(mode='OBJECT')
		bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
		bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
		o = bpy.context.active_object
		init = 0
		for x in o.data.vertices:
			if init == 0:
				a = x.co.z
				init = 1
			elif x.co.z < a:
				a = x.co.z

		for x in o.data.vertices:
			x.co.z -= a

		o.location.z += a
		bpy.ops.object.mode_set(mode=mode)
		return {'FINISHED'}


class New(bpy.types.Operator):
	bl_idname = "machin3.new"
	bl_label = "Current file is unsaved. Start a new file anyway?"
	bl_options = {'REGISTER'}


	def execute(self, context):
		bpy.ops.wm.read_homefile(app_template="")

		return {'FINISHED'}

	def invoke(self, context, event):
		if bpy.data.is_dirty:
			return context.window_manager.invoke_confirm(self, event)
		else:
			bpy.ops.wm.read_homefile(app_template="")
			return {'FINISHED'}


class WAZOU_TRANSFORMS_OT_Apply_Clear(bpy.types.Operator):
	bl_idname = "wazou_transforms.apply_clear"
	bl_label = "Wazou Transforms"
	bl_options = {'REGISTER', 'UNDO'}

	apply_clear: EnumProperty(
		items=(('apply_location', "APPLY_LOCATION", ""),
			   ('apply_rotation', "APPLY_ROTATION", ""),
			   ('apply_scale', "APPLY_SCALE", ""),
			   ('apply_rot_scale', "APPLY_ROT_SCALE", ""),
			   ('apply_all', "APPLY_ALL", ""),
			   ('clear_all', "CLEAR_ALL", ""),
			   ),
		default='apply_location'
	)

	def execute(self, context):

		# Apply
		if self.apply_clear == 'apply_location':
			bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
		elif self.apply_clear == 'apply_rotation':
			bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
		elif self.apply_clear == 'apply_scale':
			bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
		elif self.apply_clear == 'apply_rot_scale':
			bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
		elif self.apply_clear == 'apply_all':
			bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

		# Clear
		elif self.apply_clear == 'clear_all':
			bpy.ops.object.location_clear()
			bpy.ops.object.rotation_clear()
			bpy.ops.object.scale_clear()

		return {'FINISHED'}




class Save(bpy.types.Operator):
	bl_idname = "machin3.save"
	bl_label = "Save"
	bl_description = "Save"
	bl_options = {'REGISTER'}

	def execute(self, context):
		currentblend = bpy.data.filepath

		if currentblend:
			bpy.ops.wm.save_mainfile()

			t = time.time()
			localt = time.strftime('%H:%M:%S', time.localtime(t))

			print("%s | Saved blend: %s" % (localt, currentblend))
		else:
			bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')

		return {'FINISHED'}


class SaveIncremental(bpy.types.Operator):
	bl_idname = "machin3.save_incremental"
	bl_label = "Incremental Save"
	bl_description = "Incremental Save"
	bl_options = {'REGISTER'}


	def execute(self, context):
		currentblend = bpy.data.filepath

		if currentblend:
			save_path = self.get_incremented_path(currentblend)

			# add it to the recent files list
			add_path_to_recent_files(save_path)

			if os.path.exists(save_path):
				self.report({'ERROR'}, "File '%s' exists already!\nBlend has NOT been saved incrementally!" % (save_path))
			else:
				bpy.ops.wm.save_as_mainfile(filepath=save_path)
				print("Saved blend incrementally:", save_path)
		else:
			bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')

		return {'FINISHED'}


	def get_incremented_path(self, currentblend):
		path = os.path.dirname(currentblend)
		filename = os.path.basename(currentblend)

		filenameRegex = re.compile(r"(.+)\.blend\d*$")

		mo = filenameRegex.match(filename)

		if mo:
			name = mo.group(1)
			numberendRegex = re.compile(r"(.*?)(\d+)$")

			mo = numberendRegex.match(name)

			if mo:
				basename = mo.group(1)
				numberstr = mo.group(2)
			else:
				basename = name + "_"
				numberstr = "000"

			number = int(numberstr)

			incr = number + 1
			incrstr = str(incr).zfill(len(numberstr))
			incrname = basename + incrstr + ".blend"

			return os.path.join(path, incrname)


class LoadMostRecent(bpy.types.Operator):
	bl_idname = "machin3.load_most_recent"
	bl_label = "Load Most Recent"
	bl_options = {"REGISTER"}

	def execute(self, context):
		recent_path = bpy.utils.user_resource('CONFIG', "recent-files.txt")

		try:
			with open(recent_path) as file:
				recent_files = file.read().splitlines()
		except (IOError, OSError, FileNotFoundError):
			recent_files = []

		if recent_files:
			most_recent = recent_files[0]

			# load_ui ensures the the viewport location/angle is loaded as well
			bpy.ops.wm.open_mainfile(filepath=most_recent, load_ui=True)

		return {'FINISHED'}


classes = (
	ModalOperator,
	ViewOperatorRayCast,
	AKM_MENUS_OT_delete_all_uvs,
	AKM_MENUS_OT_set_smooth_180,
	AKM_MENUS_OT_delete_all_mats,
	AKM_MENUS_OT_move_selected_to_active_collection,
	AKM_MENUS_OT_set_visibility_subd_modifier,
	AKM_MENUS_OT_set_subd_modifier_levels,
	AKM_MENUS_OT_set_visibility_mirror_modifier,
	AKM_MENUS_OT_collapse_modifiers,
	AKM_MENUS_OT_remove_modifiers,
	AKM_MENUS_OT_remove_subd_modifiers,
	AKM_MENUS_OT_splitnormals_clear,
	AKM_MENUS_OT_set_material_by_mouse_pos,
	WAZOU_RMB_PIE_MENUS_OT_test,
	WAZOU_TRANSFORMS_OT_Apply_Clear,
	WAZOU_PIVOT_OT_to_selection,
	New,
	Save,
	SaveIncremental,
	)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	simple_modal_operator.register()


def unregister():

	for cls in classes:
		bpy.utils.unregister_class(cls)

	simple_modal_operator.unregister()
