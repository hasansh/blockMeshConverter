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
                                 usage="%prog COMMAND <blockMeshDict2D> <value>",
                                 changeVersion=False,
                                 nr=2,
                                 subcommands=False,
                                 **kwargs)
    def addOptions(self):
        how=OptionGroup(self.parser,
                         "Information",
                         "Information about the case")
        self.parser.add_option_group(how)
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
    def run(self):
        if self.opts.expositive:
            print "extrude positive"
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
        mesh=BlockMesh2D('blockMeshDict2D',"ROTATEX",-0.0174533,0.0174533,5)
        # mesh.numberVertices('Number:')
        # print mesh.convertVertices()
        # print mesh.convertBlocks()
        # print mesh.convertEdges()      
        # print mesh.convertBoundaries()
        print mesh.convert2DBlockMesh()
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




