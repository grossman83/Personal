#Timing belt pulley script
#MXL and XL profile timing belts.

#####USE
#To use this simply modify the numTeeth parameter and set mxl to True for MXL type belt
#or set it to false for XL type belt. This creates only the tooth profiles and has been
#working just fine for me with my Markforged Onyx printer. Hope this is of use to others.


#COLLABORATION
#If anyone wants to collaborate to improve this I'd be happy to get some guidance/help
#adding a GUI window for it.


#COPYRIGHT / WARRANTY
#No copyright or anything. Do with this as you wish. I assume no liability for anything and
#I make no warranties.


#2018 Marc Grossman






import adsk.core, adsk.fusion, traceback, math

def run(context):
    ui = None
    try: 
        app = adsk.core.Application.get()
        ui = app.userInterface

        #create a new document
        #doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketches = rootComp.sketches;
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)


        #specific for this pulley
        ###############################PARAMETERS TO EDIT#######################################
        numTeeth = 30
        mxl = False
        ###############################PARAMETERS TO EDIT#######################################


        in2cm = 2.54
        cm2in = 1/2.54

        if(mxl):
            toothPitch = 0.080 * in2cm
            toothWidth = 0.030 * in2cm
            troughDepth = 0.018 * in2cm
            toothFullAngle = 40#degrees
            cornerRadius = 0.005 * in2cm
            varU = 0.010 * in2cm
            pulleyThickness = 0.315 * in2cm

        else:
            #for XL belt type
            toothPitch = 0.200 * in2cm
            toothWidth = 0.054 * in2cm
            troughDepth = 0.050 * in2cm
            toothFullAngle = 50#degrees
            cornerRadius = 0.015 * in2cm
            varU = 0.010 * in2cm
            pulleyThickness = 0.300 * in2cm

        #fudge factor to allow some slop.
        epsilon = 0.004 * in2cm

        
        # toothWidth = toothWidth+epsilon/2.0
        # troughDepth = troughDepth+epsilon/2.0

        toothFullAngle_rad = toothFullAngle * math.pi/180.0
        pitchDiameter = toothPitch * numTeeth / math.pi






        circles = sketch.sketchCurves.sketchCircles
        #pitchDiameterCircle = circles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), pitchDiameter/2.0)
        pulleyOD = pitchDiameter - 2.0 * varU
        # pulleyOD = pulleyOD - 2*epsilon
        pulleyODCircle = circles.addByCenterRadius(adsk.core.Point3D.create(0,0,0), pulleyOD/2.0)

        #get the profile to extrude
        prof = sketch.profiles.item(0)

        #extrude the pulley
        # Get extrude features
        extrudes = rootComp.features.extrudeFeatures
        extrude1 = extrudes.addSimple(prof, adsk.core.ValueInput.createByReal(pulleyThickness), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        body1 = extrude1.bodies.item(0)
        body1.name = "pulley_base"

        

        pt1 = adsk.core.Point3D.create(-0.5*toothWidth, pulleyOD/2.0-troughDepth,0)
        pt2 = adsk.core.Point3D.create(0.5*toothWidth, pulleyOD/2.0-troughDepth, 0)
        pt3 = adsk.core.Point3D.create(0.5*toothWidth + troughDepth * math.tan(toothFullAngle_rad/2.0), pulleyOD/2.0, 0)
        pt4 = adsk.core.Point3D.create(-0.5*toothWidth - troughDepth * math.tan(toothFullAngle_rad/2.0), pulleyOD/2.0, 0)
        

        #create wedge with which we'll cut the pulley
        #define the plane on which we'll create the sketch
        toothSketch = sketches.add(body1.faces.item(2))#the top face of the cylinder we extruded above
        lines = toothSketch.sketchCurves.sketchLines
        line1 = lines.addByTwoPoints(pt1, pt2)
        line2 = lines.addByTwoPoints(line1.endSketchPoint, pt3)
        line3 = lines.addByTwoPoints(line2.endSketchPoint, pt4)
        line4 = lines.addByTwoPoints(line3.endSketchPoint, line1.startSketchPoint)
        
        # filletRad = 0.003 * in2cm

        # arc = toothSketch.sketchCurves.sketchArcs.addFillet(line1, line1.endSketchPoint.geometry, line2, line2.startSketchPoint.geometry, filletRad)
        # arc = toothSketch.sketchCurves.sketchArcs.addFillet(line2, line2.endSketchPoint.geometry, line3, line3.startSketchPoint.geometry, filletRad)
        # arc = toothSketch.sketchCurves.sketchArcs.addFillet(line3, line3.endSketchPoint.geometry, line4, line4.startSketchPoint.geometry, filletRad)
        # arc = toothSketch.sketchCurves.sketchArcs.addFillet(line4, line4.endSketchPoint.geometry, line1, line1.startSketchPoint.geometry, filletRad)

        
        # toothProfile = toothSketch.profiles.item(0)
        coll = toothSketch.findConnectedCurves(line1)
        dirPoint = adsk.core.Point3D.create(0, pulleyOD, 0)
        offsetToothProfile = toothSketch.offset(coll, dirPoint, epsilon)
        
        oversizeToothProfile = adsk.core.ObjectCollection.create()
        oversizeToothProfile.add(toothSketch.profiles.item(0))
        oversizeToothProfile.add(toothSketch.profiles.item(2))

        
        toothCut = extrudes.addSimple(oversizeToothProfile, adsk.core.ValueInput.createByReal(-1*pulleyThickness), adsk.fusion.FeatureOperations.CutFeatureOperation)
        
        #get the axis for the circular pattern
        zAxis = rootComp.zConstructionAxis

        #create input entities for circular pattern
        inputEntities = adsk.core.ObjectCollection.create()
        inputEntities.add(toothCut)

        #create the input for the circular pattern
        circularFeats = rootComp.features.circularPatternFeatures
        circularFeatInput = circularFeats.createInput(inputEntities, zAxis)
        
        #set the quantity
        circularFeatInput.quantity = adsk.core.ValueInput.createByReal(numTeeth)
        
        #set the angle
        circularFeatInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')
        
        circularFeatInput.isSymmetric = False
        #create the circular pattern
        circularFeat = circularFeats.add(circularFeatInput)

        print('process complete')
        

    except:
        print ("problem")
        print ("debug")        
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))