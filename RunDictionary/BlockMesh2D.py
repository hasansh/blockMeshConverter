
"""Manipulate a 2 Dimensional C{blockMeshDict}"""

import re,os
import copy
from PyFoam.Basics.LineReader import LineReader
from PyFoam.RunDictionary.FileBasis import FileBasisBackup
from PyFoam.RunDictionary.BlockMesh import BlockMesh
from PyFoam.RunDictionary.ParsedBlockMeshDict import ParsedBlockMeshDict
from math import ceil
from PyFoam.Error import error

class BlockMesh2D(FileBasisBackup):
    def __init__(self, name, backup=False):
        """:param name: The name of the parameter file
           :param backup: create a backup-copy of the file
        """
        FileBasisBackup.__init__(self,name,backup=backup)
        self.parsedBlockMesh=ParsedBlockMeshDict(name)
        
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
    def convertBlocks(self):
        blocksList=self._get2DBlocks()
        tempBloksList=copy.deepcopy(blocksList)
        newBlocksList=list()
        for block in tempBloksList:
            block=block+block
            newBlocksList.append(block)
        startPattern=re.compile("^\s*blocks")
        endPattern=re.compile("^\s*\);")
        hexPattern=re.compile("^\s*(hex)\s*(\(.+\))\s+(\(\s*\d+\s+\d+\s*)(\)\s+simpleGrading\s*) (\(\s*\d+\s+\d+\s*)(\).*$)")
        hexblockPattern=re.compile("^\s*hex\s*(\(.+\))\s+\(\s*\d+\s+\d+\s+\d+\s*\).*$")
        inBlock=False
        l=self.__startProcess()
        newMesh=""
        count=0
        while l.read(self.fh):
            toPrint=l.line
            if not inBlock:
                if startPattern.match(l.line):
                    inBlock=True
            else:
                if endPattern.match(l.line):
                    inBlock=False
                else:
                    m=hexPattern.match(l.line)
                    if m!=None:
                        g=m.groups()
                        toPrint="\t %s %s %s%s %s%s" % (g[0],"("+' '.join(map(str,newBlocksList[count]))+")",g[2]+" 1",g[3],g[4]+" 1",g[5])
                        count=count+1
            newMesh+=toPrint+"\n"
        return self.__endProcess(newMesh)

    def convertVertices(self):
        """Remove comments after vertices"""

        startPattern=re.compile("^\s*vertices")
        endPattern=re.compile("^\s*\);")
        vertexPattern=re.compile("^(\s*\(\s*\S+\s+\S+\s*\)).*$")
        newvertices=self._get3DVertexes()
        inVertex=False
        newMesh=""
        stringVert=""
        l=self.__startProcess()
        count=0
        while l.read(self.fh):
            toPrint=l.line
            if not inVertex:
                if startPattern.match(l.line):
                    inVertex=True
            elif endPattern.match(l.line):
                print newvertices
                for vert in newvertices:
                    stringVert+="\t(".expandtabs(4)+' '.join(str(e) for e in vert)+")\n"
                toPrint=stringVert+toPrint
                inVertex=False

            else:
                m=vertexPattern.match(l.line)
                if m!=None:
                    toPrint=""
                    newMesh=newMesh.rstrip()
            newMesh+=toPrint+"\n"

        return self.__endProcess(newMesh)

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

# Should work with Python3 and Python2
    # def numberVertices(self, prefix="Point:"):
        # newmesh=super(BlockMesh2D,self).numberVertices(prefix)
        # l=self._BlockMesh__endProcess(newmesh,False)
        # return l
    # def convertToMeters(self):
        # return self.parsedBlockMesh.convertToMeters()
    # def blocks(self):
        # """Return a list with 4 vertices that define each block"""
        # return self.parsedBlockMesh.blocks()
    # def patches(self):
        # return self.parsedBlockMesh.patches()
    # def arcs(self):
        # return self.parsedBlockMesh.arcs()
    # def getBounds(self):
        # return self.parsedBlockMesh.getBounds()
    # def typicalLength(self):
        # return self.parsedBlockMesh.typicalLength()
    


    # def __endProcess(self, newMesh,getContent=True):
        # return self.__endProcess(newMesh,getContent)

    # def refineMesh(self,factors,offset=(0,0,0),getContent=False,addOld=True):
        # """Refine the Mesh by multiplying the number of cells in the blocks
        # :param factors: either a scalar to scale in all directions or a
        # tuple with the value for each direction
        # :param offset: an optional tuple for an additionnal offset value
        # for each direction
        # :param getContent: Return the contents instead of writing a fil. Main purpose
        # of this parameter is not to break compatibility with old versions"""

        # if type(factors)!=tuple:
            # f=(factors,factors,factors)
        # else:
            # f=factors

        
    # def mergeVertices(self,other):
        # """Merge in the vertexes from another mesh after our own vertexes"""

        # otherVert=BlockMesh(other)._getVertexes()

        # startPattern=re.compile("^\s*vertices")
        # endPattern=re.compile("^\s*\);")
        # vertexPattern=re.compile("^\s*\(\s*(\S+)\s+(\S+)\s+(\S+)\s*\).*$")

        # inVertex=False
        # newMesh=""
        # l=self.__startProcess()

        # while l.read(self.fh):
            # toPrint=l.line
            # if not inVertex:
                # if startPattern.match(l.line):
                    # inVertex=True
            # elif endPattern.match(l.line):
                # inVertex=False
                # tmp=toPrint
                # toPrint=""
                # for k in otherVert:
                    # toPrint+=otherVert[k][1]+"\n"
                # toPrint+=tmp
            # else:
                # m=vertexPattern.match(l.line)
                # if m!=None:
                    # if m.groups() in otherVert:
                        # del otherVert[m.groups()]
            # newMesh+=toPrint+"\n"

        # return self.__endProcess(newMesh)
