"""
Application-class that implements pyFoamBlockMeshRewrite.py
"""
from optparse import OptionGroup
from PyFoam.Applications.PyFoamApplication import PyFoamApplication
from PyFoam.Basics.RestructuredTextHelper import RestructuredTextHelper
from PyFoam.Basics.FoamOptionParser import Subcommand
from RunDictionary.BlockMesh2D import BlockMesh2D
from PyFoam.Basics.DataStructures import *
from os import path
import sys,re
from PyFoam.ThirdParty.six import print_


class BlockMeshConverter(PyFoamApplication):
    def __init__(self,
                args=None,
                 **kwargs):
        description="""\
This utility manipulates blockMeshDict. Manipulation happens on a textual basis .
This means that the utility assumes that the blockMeshDict is sensibly formated
(this means for instance that there is only one block/vertex per line and they only
go over one line
                """
        PyFoamApplication.__init__(self,
                                 args=args,
                                 description=description,
                                 usage="%prog <blockMeshDict2D>",
                                 changeVersion=False,
                                 nr=1,
                                 subcommands=False,
                                 **kwargs)
    def addOptions(self):
        how=OptionGroup(self.parser,
                         "How",
                         "Extursion type of 2D blockMesh")
        self.parser.add_option_group(how)
        value=OptionGroup(self.parser,
                          "Value",
                          "Values of extrusion")
        how.add_option("--extrude-positive",
                        action="store_true",
                        dest="expositive",
                        default=False,
                        help="Extrude 2D blockMesh in positive direction")

        how.add_option("--extrude-negative",
                        action="store_true",
                        dest="exnegative",
                        default=False,
                        help="Extrude 2D blockMesh in negative direction")

        how.add_option("--extrude-middle",
                        action="store_true",
                        dest="exmiddle",
                        default=False,
                        help="Extrude 2D blockMesh in both positive and negative directions")

        how.add_option("--rotate-positive",
                        action="store_true",
                        dest="rtpositive",
                        default=False,
                        help="Rotates 2D blockMesh in positive direction")

        how.add_option("--rotate-negative",
                        action="store_true",
                        dest="rtnegative",
                        default=False,
                        help="Rotates 2D blockMesh in negative direction")

        how.add_option("--rotate-middle",
                        action="store_true",
                        dest="rtmiddle",
                        default=False,
                        help="Rotates 2D blockMesh in both positive and  negative directions")
        value.add_option("--front",
                         action="store",
                         type="float",
                         default=0,
                         dest="frontvalue",
                         help="Enter the value of extrusion in positive direction")
        value.add_option("--back",
                         action="store",
                         type="float",
                         default=0,
                         dest="backvalue",
                         help="Enter the value of extrusion in negative direction")
        value.add_option("--division",
                         action="store",
                         type="int",
                         default=1,
                         dest="division",
                         help="Enter the value of extrusion in negative direction")
        value.add_option("--dest",
                         action="store",
                         type="str",
                         default="blockMeshDict",
                         dest="destination",
                         help="Enter the name of converted blockMeshDict")
    def run(self):
        if self.opts.expositive:
            bmFile=self.parser.getArgs()[0]
            if not path.exists(bmFile):
                self.error(bmFile,"not found")
            outbmFile=path.join(path.dirname(bmFile),self.opts.destination)
            if(self.opts.frontvalue is not 0 or self.opts.backvalue is not 0):
                try:
                    mesh=BlockMesh2D(self.parser.getArgs()[0],
                                     "EXTRUDE",
                                     -self.opts.backvalue,
                                     self.opts.frontvalue,
                                     self.opts.division
                                    )
                    open(outbmFile,"w").write(mesh.convert2DBlockMesh())

                except:
                    raise
        if self.opts.exnegative:
            print "extrude negative"
        if self.opts.exmiddle:
            print "extrude middle"
        if self.opts.rtpositive:
            print "rotate positive"
        if self.opts.rtnegative:
            print "rotate negative"
        if self.opts.rtmiddle:
            print "rotate middle"
        # mesh=BlockMesh2D('blockMeshDict2D',"ROTATEX",-8,a,5)
       # # mesh.numberVertices('Number:')
        # # print mesh.convertVertices()
        # # print mesh.convertBlocks()
        # # print mesh.convertEdges()      
        # # print mesh.convertBoundaries()
        # print mesh.convert2DBlockMesh()
        # for item in mesh.convertBoundaries():
            # print item
 
        # for boundary in mesh.convertBoundaries():
            # if type(boundary) is DictProxy:
                # for key, value in  boundary.items():
                    # if type(value) is list:
                        # print value



        # for item in mesh.convertEdges():
            # print item
        # mesh.get2DBlocks() 
        # for k in mesh.getVertexes():
            # print k[0],k[1]




