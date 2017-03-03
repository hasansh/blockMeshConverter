"""
Application-class that implements pyFoamBlockMeshRewrite.py
"""
from optparse import OptionGroup
from PyFoam.Applications.PyFoamApplication import PyFoamApplication
from PyFoam.Basics.RestructuredTextHelper import RestructuredTextHelper
from PyFoam.Basics.FoamOptionParser import Subcommand
from RunDictionary.BlockMesh2D import BlockMesh2D
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
                                 usage="%prog COMMAND <blockMeshDict>",
                                 changeVersion=False,
                                 subcommands=False,
                                 **kwargs)
    def addOptions(self):
        print "There is not options yet!!"
    def run(self):
        print "Program is running"
        mesh=BlockMesh2D('blockMeshDict2D')
        mesh.numberVertices('Number:')
        print mesh.convertVertices()

        # for k in mesh.getVertexes():
            # print k[0],k[1]




