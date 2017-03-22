# blockMeshConverter
BlockMeshConverter is an python application compatible with PyFoam for converting 2D BlockMeshDict to a 3d blockMesh dict appropriate for blockMesh utility of OpenFOAM. 
## Usage
To use it you need to create a blockMeshDict similar to standard blockMeshDict in OpenFOAM. However instead of using 3D points and blocks you need to define 2D poinst and blocks and you need to define boundaries as edges instead of faces.
![Two dimensional block definition](/images/2DBlocks.png)
Then using the following command you will be able to extrued or rotate 2D blockMesh to 3D blockMeshDict. 

`python pyFoamBlockMeshConverter.py --extrude --front 0.5 --back 0.5 --division 5 --dest ~/path/to/desitnation /path/to/blockMesh2D`
