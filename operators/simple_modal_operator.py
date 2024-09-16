import bpy
from bpy.props import IntProperty, FloatProperty


class ModalOperator(bpy.types.Operator):
	"""Move an object with the mouse, example"""
	bl_idname = "object.modal_operator"
	bl_label = "Simple Modal Operator"

	first_mouse_x = IntProperty()
	first_value = FloatProperty()

	def modal(self, context, event):
		if event.type == 'MOUSEMOVE':
			delta = self.first_mouse_x - event.mouse_x
			context.object.location.x = self.first_value + delta * 0.01

		elif event.type == 'G':
			self.report({'INFO'}, "G")
			context.object.location.x = self.first_value
			return {'CANCELLED'}

		elif event.type == 'LEFTMOUSE':
			return {'FINISHED'}

		elif event.type in {'RIGHTMOUSE', 'ESC'}:
			context.object.location.x = self.first_value
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

# class ModalOperator(bpy.types.Operator):
# 	"""Move an object with the mouse, example"""
# 	bl_idname = "object.modal_operator"
# 	bl_label = "Simple Modal Operator"

# 	first_mouse_x: bpy.props.IntProperty()
# 	first_value: bpy.props.FloatProperty()

# 	def modal(self, context, event):
# 		if event.type == 'MOUSEMOVE':
# 			delta = self.first_mouse_x - event.mouse_x
# 			context.object.location.x = self.first_value + delta * 0.01
# 			bpy.context.window.cursor_modal_set("HAND")
# 			bpy.context.window.cursor_set("HAND")

# 		elif event.type == 'LEFTMOUSE':
# 			return {'FINISHED'}

# 		elif event.type in {'RIGHTMOUSE', 'ESC'}:
# 			context.object.location.x = self.first_value
# 			bpy.context.window.cursor_modal_restore()
# 			bpy.context.window.cursor_modal_set("DEFAULT")
# 			bpy.context.window.cursor_set("DEFAULT")
# 			return {'CANCELLED'}

# 		return {'RUNNING_MODAL'}

# 	def invoke(self, context, event):
# 		if context.object:
# 			self.first_mouse_x = event.mouse_x
# 			self.first_value = context.object.location.x
			
# 			context.window_manager.modal_handler_add(self)
# 			return {'RUNNING_MODAL'}
# 		else:
# 			self.report({'WARNING'}, "No active object, could not finish")
# 			return {'CANCELLED'}


# class ModalOperator(bpy.types.Operator):
# 	"""Allow GG operator"""
# 	bl_idname = "object.modal_operator"
# 	bl_label = "Simple Modal Operator"

# 	count=0

# 	def modal(self, context, event):
# 		self.count +=1
# 		if self.count ==1:
# 			bpy.ops.transform.translate('INVOKE_DEFAULT')

# 		elif event.type == 'G':
# 			bpy.ops.transform.rotate('INVOKE_DEFAULT')
# 			return {'CANCELLED'}

# 		elif event.type == 'LEFTMOUSE':
# 			return {'FINISHED'}

# 		elif event.type in {'RIGHTMOUSE', 'ESC'}:
# 			return {'CANCELLED'}

# 		return {'RUNNING_MODAL'}

# 	def invoke(self, context, event):
# 		if context.object:

# 			context.window_manager.modal_handler_add(self)
# 			return {'RUNNING_MODAL'}
# 		else:
# 			self.report({'WARNING'}, "No active object, could not finish")
# 			return {'CANCELLED'}


def register():
	bpy.utils.register_class(ModalOperator)

def unregister():
	bpy.utils.unregister_class(ModalOperator)