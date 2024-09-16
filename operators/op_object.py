import bpy

class AKM_MENUS_OT_clear_split_normals(bpy.types.Operator):
	"""    Clear custom split normals on selected objects"""

	bl_idname = 'akm_menus.clear_split_normals'
	bl_label = "Clear custom split normals"
	bl_options = {'REGISTER'}


	def invoke(self, context, event):
		selection = bpy.context.selected_objects

		for obj in selection:
			if obj.type != 'MESH':
				continue
			
			bpy.context.view_layer.objects.active = obj
			bpy.ops.mesh.customdata_custom_splitnormals_clear()

		return {'FINISHED'}


class AKM_MENUS_OT_select_objects_split_normals(bpy.types.Operator):
	"""    Select objects with split normals"""

	bl_idname = 'akm_menus.select_objects_split_normals'
	bl_label = "Select objects with split normals"
	bl_options = {'REGISTER'}


	def invoke(self, context, event):
		

		return {'FINISHED'}




classes = (
	AKM_MENUS_OT_clear_split_normals,
	AKM_MENUS_OT_select_objects_split_normals,
	)


def register():
	for cls in classes:
		bpy.utils.register_class(cls)


def unregister():

	for cls in classes:
		bpy.utils.unregister_class(cls)