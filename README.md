# blockMeshConverter
BlockMeshConverter is a python application compatible with [PyFoam](https://pypi.org/project/PyFoam/0.6.5/) for converting 2D BlockMeshDict to a 3D blockMeshDict appropriate for blockMesh utility of OpenFOAM C++ ToolBox. The aim of this applications is to make the process of mesh generation easier for OpenFOAM users. This applications is released as one of the official applications of [PyFoam 0.6.9](https://github.com/Unofficial-Extend-Project-Mirror/openfoam-extend-Breeder-other-scripting-PyFoam/blob/master/ReleaseNotes)
## Usage
To use it you need to create a blockMeshDict similar to standard blockMeshDict in OpenFOAM. However instead of using 3D points and blocks you need to define 2D poinst and blocks and you need to define boundaries as edges instead of faces.
![Two dimensional block definition](/images/2DBlocks.png)
Then using the following command you will be able to extrued or rotate 2D blockMesh to 3D blockMeshDict. 

`python pyFoamBlockMeshConverter.py --extrude --distance-front 0.5 --distance-back 0.5 --division 5 --front-back-type wedge --dest ~/path/to/desitnation /path/to/blockMesh2D`
