'''
The MIT License (MIT)

Copyright (c) [2016] [Islam Almusaly]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

bl_info = {
    "name": "Fingers Animation",
    "description": "Import fingers animation.",
    "author": "Islam Almusaly",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "View3D > Tool Shelf > Misc > Fingers Animation",
    "warning": "", # used for warning icon and text in addons panel
    "support": "COMMUNITY",
    "category": "Animation"}

import bpy
import math

hightestFrame = 0

def importFingersAnimation(path):
    try:
        i = 0
        fingersAnimation = list()
        # parse the file
        file = open(path, "r")
        lines = file.read().split("#")
        for line in lines:
            finger = list()
            words = line.split("-")
            for word in words:
                keyframes = word.split(",")
                if len(keyframes) > 1:
                    keyframe = list()
                    keyframe.append( (float(keyframes[0])/786.0) * -2.4 + 2.3)
                    keyframe.append( (float(keyframes[1])/1024.0) * -2.6 + 2.7)
                    keyframe.append( float(keyframes[2]) )
                    finger.append( keyframe )
            i += 1
            if i != 6:
                fingersAnimation.append(finger)
        file.close()
        createFingersAnimation(fingersAnimation)
    except:
        pass

def createFingersAnimation(fingersAnimation):
    try:
        fingersObjects = list()
        side = 'R'
        fingers = ['finger_thumb.'+side,'finger_index.'+side,'finger_middle.'+side,'finger_ring.'+side,'finger_pinky.'+side]
        #bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.add(type='EMPTY')
        holder = bpy.context.object
        holder.name = 'fingers.'+side
        for finger in fingers:
            bpy.ops.object.add(type='EMPTY')
            ob = bpy.context.object
            ob.name = finger
            ob.empty_draw_type = 'CIRCLE'
            ob.empty_draw_size = 0.2
            ob.parent = holder
            fingersObjects.append(ob)
            
        scn = bpy.context.scene
        fps = scn.render.fps
        i = 0
        for fingerAnimation in fingersAnimation:     
            obj = fingersObjects[i]
            obj.animation_data_clear()
            obj.animation_data_create()
            obj.animation_data.action = bpy.data.actions.new(name="MyAction")
            
            fcux = obj.animation_data.action.fcurves.new(data_path="location", index=0)
            fcuy = obj.animation_data.action.fcurves.new(data_path="location", index=1)
            fcuz = obj.animation_data.action.fcurves.new(data_path="location", index=2)
            
            icux = fcux.keyframe_points
            icuy = fcuy.keyframe_points
            icuz = fcuz.keyframe_points
            
            k = fingerAnimation[0]
            preFrame = int(round(k[2] * fps))
            for keyframe in fingerAnimation:
                frame = int(round(keyframe[2] * fps))
                if preFrame != frame and preFrame < frame:
                    icux.insert(frame,keyframe[0])
                    icuz.insert(frame,keyframe[1])
                    icuy.insert(frame,0)
                    preFrame = frame + 1
                    global hightestFrame
                    if hightestFrame < frame:
                        hightestFrame = frame 
            i += 1
        scn.frame_end = hightestFrame
    except:
        pass

class FingersAnimation(bpy.types.Panel):
    '''This is Islam's tool'''
    bl_label = "Fingers Animation"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    def draw(self, context):
        scn = context.scene
        layout = self.layout
        row = layout.row()
        row.operator("import.fa")

class ImportFingersAnimation(bpy.types.Operator):
    bl_idname = "import.fa"
    bl_label = "Import Fingers Animation"

    filepath = bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        try:
            importFingersAnimation(self.filepath)
        except:
            pass
        return {'FINISHED'}

    def invoke(self, context, event):
        try:
            context.window_manager.fileselect_add(self)
        except:
            pass
        return {'RUNNING_MODAL'}

def register():
    bpy.utils.register_class(ImportFingersAnimation)
    bpy.utils.register_class(FingersAnimation)
def unregister():
    bpy.utils.unregister_class(FingersAnimation)
    bpy.utils.unregister_class(ImportFingersAnimation)

if __name__ == "__main__":
    register()