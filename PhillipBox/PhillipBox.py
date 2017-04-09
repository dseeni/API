#Author-PhilippNox
#Description-NiceBox (Nicebox.one)

import adsk.core, adsk.fusion, adsk.cam, traceback, os, tempfile

app = adsk.core.Application.get()
ui  = app.userInterface
design = app.activeProduct
unitsMgr = design.unitsManager
rootComp = adsk.fusion.Component.cast(design.rootComponent)
allOccs = rootComp.occurrences





wall = 0.3
h = 10
w = 10
d = 10
kerf = 0.3
shiftTotal = 1.5
shiftTop    = shiftTotal
shiftBack   = shiftTotal
shiftBottom = shiftTotal
shiftFront  = shiftTotal

sheetAlpha = 0.3

sheetZ = (w-2*wall)*sheetAlpha/2                              #2
sheetXBase = (d-2*wall-shiftFront-shiftBack)*sheetAlpha/2     #1
sheetXFront = (h-2*wall-shiftTop-shiftBottom)*sheetAlpha/2    #1

conerFront  = d/2-wall-shiftFront #-(wall-kerf)
conerBack   = d/2-wall-shiftBack

def createNewComponent():
    # Get the active design.
    app.activeProduct
    newOcc = allOccs.addNewComponent(adsk.core.Matrix3D.create())
    return newOcc.component

root = createNewComponent() 
features = root.features
extrudes = root.features.extrudeFeatures

def run(context):
    ui = None   
    try:
       # ui.messageBox('Hello script')
        base(shiftBottom)
        base(h-wall-shiftTop)
        left((w-wall)/2)
        left(-(w-wall)/2-wall)
        back(conerBack)
        back(-conerFront-wall)
        
        print(root.bRepBodies.count)
        
        
        
        #Cut
        CombineCutFeats = features.combineFeatures          
        
        #Cut Rigth
        
        
        ToolBodies = adsk.core.ObjectCollection.create()
        ToolBodies.add(root.bRepBodies.item(0))
        ToolBodies.add(root.bRepBodies.item(1))
        ToolBodies.add(root.bRepBodies.item(4))
        ToolBodies.add(root.bRepBodies.item(5))
        
        CombineCutInput = root.features.combineFeatures.createInput(root.bRepBodies.item(2), ToolBodies )
        CombineCutInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        CombineCutInput.isKeepToolBodies = True
        CombineCutFeats.add(CombineCutInput)
        
        #Cut Left
        CombineCutInput = root.features.combineFeatures.createInput(root.bRepBodies.item(3), ToolBodies )
        CombineCutInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        CombineCutInput.isKeepToolBodies = True
        CombineCutFeats.add(CombineCutInput)
        
        #Cut Front
        ToolBodies = adsk.core.ObjectCollection.create()
        ToolBodies.add(root.bRepBodies.item(0))
        ToolBodies.add(root.bRepBodies.item(1))
        
        CombineCutInput = root.features.combineFeatures.createInput(root.bRepBodies.item(4), ToolBodies )
        CombineCutInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        CombineCutInput.isKeepToolBodies = True
        CombineCutFeats.add(CombineCutInput)
        
        #Cut back
        ToolBodies = adsk.core.ObjectCollection.create()
        ToolBodies.add(root.bRepBodies.item(0))
        ToolBodies.add(root.bRepBodies.item(1))
        
        CombineCutInput = root.features.combineFeatures.createInput(root.bRepBodies.item(5), ToolBodies )
        CombineCutInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        CombineCutInput.isKeepToolBodies = True
        CombineCutFeats.add(CombineCutInput)
        
        print(root.bRepBodies.count)
        
        print(root.sketches.count)
        
    
        DXFForCut()
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

    
def back(offset):

    sketches = root.sketches
    planeXY = root.xYConstructionPlane
    sketch = sketches.add(planeXY)
    
    lines = sketch.sketchCurves.sketchLines   
    
    lines.addTwoPointRectangle(adsk.core.Point3D.create(-(w-wall)/2,h,offset),adsk.core.Point3D.create((w-wall)/2,0,offset))
    # sheetXFront for left
    lines.addCenterPointRectangle(adsk.core.Point3D.create(-(w-wall)/2,h/2,offset),adsk.core.Point3D.create(-(w-wall)/2-wall,h/2+sheetXFront,offset))
    # sheetXFront for Rigth
    lines.addCenterPointRectangle(adsk.core.Point3D.create((w-wall)/2,h/2,offset),adsk.core.Point3D.create((w-wall)/2+wall,h/2+sheetXFront,offset))
    
    extrudes = root.features.extrudeFeatures
    #prof = sketch.profiles[0]
    
    profs = adsk.core.ObjectCollection.create()
        
    for prof in sketch.profiles:
        profs.add(prof)
        
    extrudeInput = extrudes.createInput(profs, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distExtrude = adsk.core.ValueInput.createByReal(wall)   
    extrudeInput.setDistanceExtent(False, distExtrude)
    return extrudes.add(extrudeInput)

def left(offset):
    sketches = root.sketches
    planeYZ = root.yZConstructionPlane
    sketch = sketches.add(planeYZ)
    
    lines = sketch.sketchCurves.sketchLines
    
    lines.addTwoPointRectangle(adsk.core.Point3D.create(d/2,h,offset),adsk.core.Point3D.create(-d/2,0,offset))
    
    extrudes = root.features.extrudeFeatures
    #prof = sketch.profiles[0]
    
    profs = adsk.core.ObjectCollection.create()
        
    for prof in sketch.profiles:
        profs.add(prof)
        
    extrudeInput = extrudes.createInput(profs, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distExtrude = adsk.core.ValueInput.createByReal(wall)   
    extrudeInput.setDistanceExtent(False, distExtrude)
    return extrudes.add(extrudeInput)


def base(offset):
    sketches = root.sketches
    planeXZ = root.xZConstructionPlane
    sketch = sketches.add(planeXZ)
    
    lines = sketch.sketchCurves.sketchLines
    
    
      
    #   half of base from origin to front
    lines.addTwoPointRectangle(adsk.core.Point3D.create(-(w-wall)/2,0,offset),adsk.core.Point3D.create((w-wall)/2,conerFront,offset))
    #   half of base from origin to back        
    lines.addTwoPointRectangle(adsk.core.Point3D.create(-(w-wall)/2,0,offset),adsk.core.Point3D.create((w-wall)/2,-conerBack,offset))
    # sheetZ for front
    lines.addCenterPointRectangle(adsk.core.Point3D.create(0,conerFront,offset),adsk.core.Point3D.create(sheetZ,conerFront-wall,offset))
    # sheetZ for back
    lines.addCenterPointRectangle(adsk.core.Point3D.create(0,-conerBack,offset),adsk.core.Point3D.create(sheetZ,-conerBack-wall,offset))
    # sheetXBase for left
    lines.addCenterPointRectangle(adsk.core.Point3D.create(-(w-wall)/2,0,offset),adsk.core.Point3D.create((-(w-wall)/2)-wall,sheetXBase,offset))   
    # sheetXBase for Rigth
    lines.addCenterPointRectangle(adsk.core.Point3D.create((w-wall)/2,0,offset),adsk.core.Point3D.create(((w-wall)/2)+wall,sheetXBase,offset))   
  
    extrudes = root.features.extrudeFeatures
    #prof = sketch.profiles[0]
    
    profs = adsk.core.ObjectCollection.create()
        
    for prof in sketch.profiles:
        profs.add(prof)
        
    extrudeInput = extrudes.createInput(profs, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distExtrude = adsk.core.ValueInput.createByReal(wall)   
    extrudeInput.setDistanceExtent(False, distExtrude)
    return extrudes.add(extrudeInput)
        
def DXFForCut():
    #testBody = root.bRepBodies.item(4)
   # print (root.bRepBodies)
    bodies = adsk.core.ObjectCollection.create()
    for item in root.bRepBodies:
        bodies.add.roo
        comp_obj = face.body.parentComponent
        sketch = comp_obj.sketches.add(face)
        sketch.name = "DXF" + item
        sketch_lines_world = sketch.project(face)
    print(testBody.faces.count)
    face = testBody.faces.item(21)
    
    comp_obj = face.body.parentComponent
    sketch = comp_obj.sketches.add(face)
    sketch.name = "DXF"
    sketch_lines_world = sketch.project(face)
    #tmp_dir = tempfile.TemporaryDirectory()
    #ui.messageBox(tmp_dir.name)
    #print(tmp_dir.name)

    #perimeter_dxf_path = os.path.join(tmp_dir, 'perimeter_sketch.dxf')
    #sketch_lines_world.saveAsDXF(perimeter_dxf_path)
    
    #Have the table file selected.
#    dialog = ui.createFileDialog()
#    dialog.filter = 'DXF files (*.dxf);;All files (*.*)'
#    dialog.initialDirectory = os.path.dirname(os.path.realpath(__file__))
#    if dialog.showSave() != adsk.core.DialogResults.DialogOK:
#        return
##        
#    filename = dialog.filename
#    perimeter_dxf_path = os.path.join(filename, 'perimeter_sketch.dxf')
#    print(perimeter_dxf_path)
#    sketch_lines_world.saveAsDXF(perimeter_dxf_path)
#    sketch_lines_world.saveAsDXF(   )

#pop out file dialog to save the DXF    
#    fileDialog = ui.createFileDialog()
#    fileDialog.isMultiSelectEnabled = False
#    fileDialog.title = "Export to DXF"
#    fileDialog.filter = 'DXF files (*.dxf)'
#    fileDialog.filterIndex = 0    
#    dialogResult = fileDialog.showSave()
#    if dialogResult == adsk.core.DialogResults.DialogOK:
#        filename = fileDialog.filename
#    else:
#        return   
    
#    fileDialog = ui.createFileDialog()
#    fileDialog.isMultiSelectEnabled = False
#    fileDialog.title = "Export to DXF"
#    fileDialog.filter = 'DXF files (*.dxf)'
#    fileDialog.filterIndex = 0    
#    dialogResult = fileDialog.showSave()
#    if dialogResult == adsk.core.DialogResults.DialogOK:
#        filename = fileDialog.filename
#    else:
#        return       
#    
#    sketch.saveAsDXF(filename + sketch.name + '.dxf')
#    sketch_lines_world.name("TEST")
#        
#    #comp_obj.sketches.item(1).name("TEST")
#    sketch = root.sketches.itemByName("Sketch7")
#    sketch.name = "TEST"
#    