
"""Manipulate a 2 Dimensional C{blockMeshDict}"""

import re,os
import copy
from PyFoam.Basics.LineReader import LineReader
from PyFoam.RunDictionary.FileBasis import FileBasisBackup
from PyFoam.RunDictionary.BlockMesh import BlockMesh
from PyFoam.RunDictionary.ParsedBlockMeshDict import ParsedBlockMeshDict
from PyFoam.Basics.DataStructures import *
from math import ceil
from PyFoam.Error import error
class BlockMeshEdge(object):
    def __init__(self, start, end, center, points):
        self.start=start
        self.end=end
        self.center=center
        self.points=copy.deepcopy(points)
        if(center==None and points!=None):
            self.edgeType='spline'
        else:
            self.edgeType='arc'

    def __repr__(self):
        result=""
        if self.edgeType=='spline':
            result='\t'+"spline"+' '+str(self.start)+' '+str(self.end)+"\n\t("
            for point in  self.points:
                result+='\n\t\t\t'+"("+' '.join(str(n) for n in point)+ ")"
            result+='\n\t'+")"
        elif self.edgeType=='arc':
            result='\t'+"arc"+' '+str(self.start)+' '+str(self.end)+"  ("+' '.join(str(n) for n in self.center)+ ")"
        return result
    def __str__(self):
        result=""
        if self.edgeType=='spline':
            result='\t'+"spline"+' '+str(self.start)+' '+str(self.end)+"\n\t("
            for point in  self.points:
                result+='\n\t\t\t'+"("+' '.join(str(n) for n in point)+ ")"
            result+='\n\t'+")"
        elif self.edgeType=='arc':
            result='\t'+"arc"+' '+str(self.start)+' '+str(self.end)+"  ("+' '.join(str(n) for n in self.center)+ ")"
        return result
class BlockMeshBoundary(object):
    def __init__(self, name, boundaryType, faces):
        self.name=name
        self.boundaryType=boundaryType
        self.faces=faces

    def __repr__(self):
        result='\t'+self.name+'\n\t'+"{"+'\n\t\t'+"type "+self.boundaryType+";"+'\n\t\t'+"faces"+"\n\t\t("
        for face in  self.faces:
            result+='\n\t\t\t'+"("+' '.join(str(n) for n in face)+ ")"
        result+='\n\t\t'+");"+"\n\t}"
        return result
    def __str__(self):
        result='\t'+self.name+'\n\t'+"{"+'\n\t\t'+"type "+self.boundaryType+";"+'\n\t\t'+"faces"+"\n\t\t("
        for face in  self.faces:
            result+='\n\t\t\t'+"("+' '.join(str(n) for n in face)+ ")"
        result+='\n\t\t'+");"+"\n\t}"
        return result


class BlockMesh2D(FileBasisBackup):
    def __init__(self, name, backup=False):
        """:param name: The name of the parameter file
           :param backup: create a backup-copy of the file
        """
        FileBasisBackup.__init__(self,name,backup=backup)
        self.parsedBlockMesh=ParsedBlockMeshDict(name)
        self.vertexNum=len(self.parsedBlockMesh["vertices"])

    def convert2DBlockMesh(self):
        newMesh=self._get2DMesh()
        newMesh=self.convertVertices(newMesh)
        newMesh=self.convertBlocks(newMesh)
        newMesh=self.convertEdges(newMesh)
        newMesh=self.convertBoundaries(newMesh)
        return self.__endProcess(newMesh,True)

    def _get2DMesh(self):
        mesh=""
        l=self.__startProcess()
        while l.read(self.fh):
            mesh+=l.line+'\n'
        return mesh

    def _getVertexes(self):
        """Get a dictionary with the 3 components of each vertex as keys
        and the 'raw' line as the value"""
        try:
            from collections import OrderedDict
            result=OrderedDict()
        except ImportError:
            error("This python-version doesn't have OrderedDict in library collections. Can't go on''")

        startPattern=re.compile("^\s*vertices")
        endPattern=re.compile("^\s*\);")
        vertexPattern=re.compile("^\s*\(\s*(\S+)\s+(\S+)\s+(\S+)\s*\).*$")

        inVertex=False
        l=self.__startProcess()

        cnt=0
        while l.read(self.fh):
            if not inVertex:
                if startPattern.match(l.line):
                    inVertex=True
            elif endPattern.match(l.line):
                inVertex=False
            else:
                m=vertexPattern.match(l.line)
                if m!=None:
                    result[m.groups()]=(cnt,l.line)
                    cnt+=1

        return result

    def _get3DVertexes(self):
        verticeslist=self._get2DVertexes()

        vertices=copy.deepcopy(verticeslist)
        newvertices=list()
        for vertice in vertices:
            vertice.extend([0])
            newvertices.append(vertice)
        vertices=self.parsedBlockMesh["vertices"]
        for vertice in vertices:
            vertice.extend([5])
            newvertices.append(vertice)
        return newvertices
    def _get2DVertexes(self):
        return self.parsedBlockMesh["vertices"]

    def _get2DBlocks(self) :
        blocksRawList=self.parsedBlockMesh["blocks"]
        blocksList=list()
        for index, value in enumerate(blocksRawList):
            if value=='hex':
                blocksList.append(blocksRawList[index+1])
        return blocksList

    def _get2DEdges(self):
        edgesRawList=self.parsedBlockMesh["edges"]
        edgesList=list()
        for index,value in enumerate(edgesRawList):
            if value=='spline':
                newEdge=BlockMeshEdge(edgesRawList[index+1],edgesRawList[index+2],None,edgesRawList[index+3])
                edgesList.append(newEdge)
            elif value=='arc':
                newEdge=BlockMeshEdge(edgesRawList[index+1],edgesRawList[index+2],edgesRawList[index+3],None)
                edgesList.append(newEdge)
        return edgesList

    def _get3DEdges(self):
        edgesList=self._get2DEdges()
        newEdgesList=list()
        for edge in edgesList:
            if edge.edgeType=='spline':
                pointsList=list()
                for edgepoint in edge.points:
                    pointsList.append(edgepoint+[5])
                newEdgesList.append(BlockMeshEdge(edge.start,edge.end,edge.center,pointsList))
                pointsList=list()
                for edgepoint in edge.points:
                    pointsList.append(edgepoint+[0])
                newEdgesList.append(BlockMeshEdge(edge.start+3,edge.end+3,edge.center,pointsList))
            if edge.edgeType=='arc':
                newEdgesList.append(BlockMeshEdge(edge.start,edge.end,edge.center+[0],None))
                newEdgesList.append(BlockMeshEdge(edge.start+self.vertexNum,edge.end+self.vertexNum,edge.center+[5],None)
)
        return newEdgesList
    def _get2DBoundaries(self):
        boundariesRawList=self.parsedBlockMesh["boundary"]
        boundariesList=list()
        name=""
        faces=list()
        boundaryType=""
        for index, item in enumerate(boundariesRawList):
            if type(item) is str:
                name=item
                for key, value in  boundariesRawList[index+1].items():
                    if type(value) is list:
                        faces=value
                    elif type(value) is str:
                        boundaryType=value
                boundariesList.append(BlockMeshBoundary(name,boundaryType,faces))

        return boundariesList
    def _get3DBoundaries(self):
        boundariesList=self._get2DBoundaries()
        newBoundariesList=list()
        for boundary  in boundariesList:
            boundaryFaces=list()
            for face in boundary.faces:
                newFace=list()
                for point in reversed(face):
                    newFace.append(point+self.vertexNum)
                face=face+newFace
                boundaryFaces.append(face)

            newBoundariesList.append(BlockMeshBoundary(boundary.name,boundary.boundaryType,boundaryFaces))
        return newBoundariesList
    def convertBoundaries(self,mesh):
        boundariesList=self._get3DBoundaries()
        # l=self.__startProcess()
        inBoundary=False
        inFace=False
        startPattern=re.compile("^\s*boundary")
        facestartPattern=re.compile("^\s*faces")
        endPattern=re.compile("^\s*\);")
        newMesh=""
        for line in  mesh.splitlines():
            toPrint=line
            if not inBoundary:
                if startPattern.match(line):
                    toPrint+="\n("
                    inBoundary=True
            else:
                toPrint=""
                if not inFace:
                    if facestartPattern.match(line):
                        inFace=True
                    if endPattern.match(line):
                        for boundary in reversed(boundariesList):
                           toPrint=str(boundary)+'\n' +toPrint
                        inBoundary=False
                        toPrint+='\n);'
                else:
                    if endPattern.match(line):
                            inFace=False
                    else:
                        newMesh=newMesh.rstrip()
            newMesh+=toPrint+"\n"
        return newMesh
    def convertEdges(self,mesh):
        newEdgesList=self._get3DEdges()
        # l=self.__startProcess()
        inBlock=False
        startPattern=re.compile("^\s*edges")
        endPattern=re.compile("^\s*\);")
        edgePattern=re.compile("(^\s*edges)\s(\s*)(\);)",re.MULTILINE)
        newMesh=""
        for line in  mesh.splitlines():
            toPrint=line
            if not inBlock:
                if startPattern.match(line):
                    toPrint+="\n("
                    inBlock=True
            else:
                if endPattern.match(line):
                    toPrint='\n'+toPrint
                    for edge in reversed(newEdgesList):
                       toPrint='\n'+str(edge)+toPrint
                    toPrint="\n"+toPrint
                    inBlock=False
                else:
                    toPrint=""
                    newMesh=newMesh.rstrip()
            newMesh+=toPrint+"\n"
        return newMesh

    def convertBlocks(self,mesh):
        blocksList=self._get2DBlocks()
        tempBloksList=copy.deepcopy(blocksList)
        newBlocksList=list()
        for block in tempBloksList:
            tmpBlock=list()
            for point in block:
                tmpBlock.append(point+self.vertexNum)
            block=block+tmpBlock
            newBlocksList.append(block)
        startPattern=re.compile("^\s*blocks")
        endPattern=re.compile("^\s*\);")
        hexPattern=re.compile("^\s*(hex)\s*(\(.+\))\s+(\(\s*\d+\s+\d+\s*)(\)\s+simpleGrading\s*) (\(\s*\d+\s+\d+\s*)(\).*$)")
        hexblockPattern=re.compile("^\s*hex\s*(\(.+\))\s+\(\s*\d+\s+\d+\s+\d+\s*\).*$")
        inBlock=False
        l=self.__startProcess()
        newMesh=""
        count=0
        for line in  mesh.splitlines():
            toPrint=line
            if not inBlock:
                if startPattern.match(line):
                    inBlock=True
            else:
                if endPattern.match(line):
                    inBlock=False
                else:
                    m=hexPattern.match(line)
                    if m!=None:
                        g=m.groups()
                        toPrint="\t %s %s %s%s %s%s" % (g[0],"("+' '.join(map(str,newBlocksList[count]))+")",g[2]+" 1",g[3],g[4]+" 1",g[5])
                        count=count+1
            newMesh+=toPrint+"\n"
        return self.__endProcess(newMesh)

    def convertVertices(self, mesh):
        """Remove comments after vertices"""

        startPattern=re.compile("^\s*vertices")
        endPattern=re.compile("^\s*\);")
        vertexPattern=re.compile("^(\s*\(\s*\S+\s+\S+\s*\)).*$")
        newvertices=self._get3DVertexes()
        inVertex=False
        newMesh=""
        stringVert=""
        # l=self.__startProcess()
        count=0
        for line in  mesh.splitlines():
            toPrint=line
            if not inVertex:
                if startPattern.match(line):
                    inVertex=True
            elif endPattern.match(line):
                for vert in newvertices:
                    stringVert+="\t(".expandtabs(4)+' '.join(str(e) for e in vert)+")\n"
                toPrint=stringVert+toPrint
                inVertex=False

            else:
                m=vertexPattern.match(line)
                if m!=None:
                    toPrint=""
                    newMesh=newMesh.rstrip()
            newMesh+=toPrint+"\n"

        return newMesh

    def stripVertexNumber(self):
        """Remove comments after vertices"""

        startPattern=re.compile("^\s*vertices")
        endPattern=re.compile("^\s*\);")
        vertexPattern=re.compile("^(\s*\(\s*\S+\s+\S+\s*\)).*$")
        newvertices=self.getBlocks()
        inVertex=False
        newMesh=""
        l=self.__startProcess()
        count=0
        while l.read(self.fh):
            toPrint=l.line
            if not inVertex:
                if startPattern.match(l.line):
                    inVertex=True
            elif endPattern.match(l.line):
                inVertex=False
            else:
                m=vertexPattern.match(l.line)
                if m!=None:
                    toPrint=m.group(1)
            newMesh+=toPrint+"\n"
            # count=count+1

        return self.__endProcess(newMesh,True)

    def numberVertices(self,prefix=""):
        """Add comments with the number of the vertex after them
        :param prefix: a string to add before the number"""

        startPattern=re.compile("^\s*vertices")
        endPattern=re.compile("^\s*\);")
        vertexPattern=re.compile("^\s*\(\s*\S+\s+\S+\s*\).*$")

        inVertex=False
        newMesh=""
        l=self.__startProcess()

        cnt=0
        while l.read(self.fh):
            toPrint=l.line
            if not inVertex:
                if startPattern.match(l.line):
                    inVertex=True
            elif endPattern.match(l.line):
                inVertex=False
            else:
                m=vertexPattern.match(l.line)
                if m!=None:
                    toPrint+=" \t // "+prefix+" "+str(cnt)
                    cnt+=1
            newMesh+=toPrint+"\n"

        return self.__endProcess(newMesh,False)

    def __startProcess(self):
        l=LineReader(False)
        self.openFile()
        return l


    def __endProcess(self,newMesh,getContent=True):
        if getContent:
            self.content=newMesh
            return newMesh
        else:
            (fh,fn)=self.makeTemp()

            fh.write(newMesh)
            self.closeFile()
            fh.close()
            os.rename(fn,self.name)

