import os
from platform import node 
import Sofa
from ControllerForce import ControllerForce
from stlib3.scene import MainHeader

'''
length of the arm is 600 mm
Base radius is 30 mm
Tip radius is 7.5 mm
'''

armYoungModulus=110
armPoissonRatio=0.5
armMass=0.1279



def createScene(rootNode):
    rootNode.addObject('RequiredPlugin', pluginName=['SoftRobots','SofaSparseSolver','SofaPreconditioner','SofaPython3','SofaConstraint',
                                                     'SofaImplicitOdeSolver','SofaLoader','SofaSimpleFem','SofaBoundaryCondition','SofaEngine',
                                                     'SofaOpenglVisual', "SofaDeformable"])

    rootNode.addObject('VisualStyle',
                       displayFlags='showVisualModels hideBehaviorModels showCollisionModels hideBoundingCollisionModels hideForceFields showInteractionForceFields hideWireframe')

    rootNode.addObject('FreeMotionAnimationLoop')
    rootNode.addObject('DefaultVisualManagerLoop')

    rootNode.addObject('GenericConstraintSolver', tolerance=1e-5, maxIterations=100)

    rootNode.addObject('BackgroundSetting', color=[0, 0.168627, 0.211765, 1])
    rootNode.addObject('OglSceneFrame', style="Arrows", alignment="TopRight")

    
    ##########################################
    # FEM Model                              #
    ##########################################
    arm = rootNode.addChild('arm')
    arm.addObject('EulerImplicitSolver', name='odesolver', firstOrder=True)
    arm.addObject('SparseLDLSolver', name='preconditioner', template='CompressedRowSparseMatrixMat3x3d')

    arm.addObject('MeshVTKLoader', name='loader', filename='./mesh/arm.vtk')
    arm.addObject('TetrahedronSetTopologyContainer', position='@loader.position', tetras='@loader.tetras', name='container')

    # Add a mechanical object component to stores the DoFs of the model
    arm.addObject('MechanicalObject', name='tetras', template='Vec3')

    # Gives a mass to the model
    arm.addObject('UniformMass', totalMass=armMass)
    
    ## Implementing constitutive law of material and mass
    # Define material to be simulated by adding a ForceField component
    # This describes what internal forces are created when the object is deformed
    # Additionally, this will define how stiff or soft the material is as well as its behaviour

    arm.addObject('TetrahedronFEMForceField', template='Vec3', name='FEM', method='large', poissonRatio=armPoissonRatio,  youngModulus=armYoungModulus)

    # To facilitate the selection of DoFs, SOFA has a concept called ROI (Region of Interest).
    # The idea is that ROI component "select" all DoFS that are enclosed by their "region".
    # We use ROI here to select a group of finger's DoFs that will be constrained to stay
    # at a fixed position.

    # The arm base is in the x-y plane and the height is in the z-direction
    # box points = [xmin, ymin, zmin, xmax, ymax, zmax]
    arm.addObject('BoxROI', name='ROI', box=[-30, -30, 0, 30, 30, 10], drawBoxes=True)

    # RestShapeSpringsForceField is one way in Sofa to implement fixed point constraint.
    # Here the constraints are applied to the DoFs selected by the previously defined BoxROI
    arm.addObject('RestShapeSpringsForceField', points='@ROI.indices', stiffness=1e12)

    arm.addObject('LinearSolverConstraintCorrection')


    ##########################################
    # Cables                                 #
    ##########################################
    
    ######## Cable 0 ###########
    cable = arm.addChild('cable')
    cable.addObject('MechanicalObject',  position=[[25, 0, 0], [5, 0, 600]])

    # Add a CableConstraint object with a name.
    # the indices are referring to the MechanicalObject's positions.
    # The last index is where the pullPoint is connected.
    # By default, the Cable is controlled by displacement, rather than force.
    cable.addObject('CableConstraint', name="aCable", indices=list(range(2)), pullPoint=[25, 0, -15], valueType='force')

    # This adds a BarycentricMapping. A BarycentricMapping is a key element as it will add a bidirectional link
    # between the cable's DoFs and the finger's ones so that movements of the cable's DoFs will be mapped
    # to the finger and vice-versa;
    cable.addObject('BarycentricMapping')


    ##########################################
    # CONTROLLER                             #
    ##########################################

    # This adds a PythonScriptController that permits to programmatically implement new behavior
    # or interactions using the Python programming language. The controller is referring to a
    # file named "controller.py".
    arm.addObject(ControllerForce(node=arm))



    ##########################################
    # Visualization                          #
    ##########################################
    # In Sofa, visualization is handled by adding a rendering model.
    # add an empty child node to store this rendering model.
    armVisu = arm.addChild('visu')
    armVisu.addObject('MeshSTLLoader', name='Loader', filename='./mesh/arm.stl')
    armVisu.addObject('OglModel', src='@Loader', color=[0.7, 0.7, 1])
    armVisu.addObject('BarycentricMapping')

    return rootNode