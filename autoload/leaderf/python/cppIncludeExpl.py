#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vim
import os
import os.path
import subprocess
from leaderf.utils import *
from leaderf.explorer import *
from leaderf.manager import *

include_hints = '.include_hints'

def check_path(p):
    if os.path.exists(os.path.join(p, include_hints)):
        return True
    return False

def find_project_root(pwd):
    current = pwd
    while os.path.split(current)[1]:
        if check_path(current):
            return current
        current = os.path.split(current)[0]

    return pwd


class CppIncludeExplorer(Explorer):
    def __init__(self):
        pass

    def getContent(self, *args, **kwargs):
        project_root = find_project_root(lfEval('expand("%:p:h")'))
        working_direcotries = []
        if check_path(project_root):
            with open(os.path.join(project_root, include_hints), 'r') as fp:
                hint = fp.readlines()
                for directory in hint:
                    working_direcotries.append(os.path.join(project_root, directory.strip()))
        else:
            working_direcotries.append(project_root)
        res = []
        for directory in working_direcotries:
            result = subprocess.run(
                ['fd', '-LI', '-e', 'h', '-e', 'hpp', '-e', 'hh',
                 '--base-directory', directory],
                stdout=subprocess.PIPE, encoding='utf-8')
            res.extend([x.strip() for x in result.stdout.split('\n') if x.strip()])
        return list(set(res))

    def getStlCategory(self):
        return "CppInclude"

    def getStlCurDir(self):
        return escQuote(lfEncode(os.getcwd()))

    def isFilePath(self):
        return False


class CppIncludeExplManager(Manager):
    def __init__(self):
        super(CppIncludeExplManager, self).__init__()
        self._match_ids = []

    def _getExplClass(self):
        return CppIncludeExplorer

    def _defineMaps(self):
        lfCmd("call leaderf#CppInclude#Maps()")

    def _acceptSelection(self, *args, **kwargs):
        if len(args) == 0:
            return

        line = args[0]
        if line == "":
            return

        lfCmd("call setline(line('.'), '#include \"%s\"')" % line)
        lfCmd("call cursor(line('.'), col('$'))")

    def _cmdExtension(self, cmd):
        return True

    def _getDigest(self, line, mode):
        """
        specify what part in the line to be processed and highlighted
        Args:
            mode: 0, 1, 2, return the whole line
        """
        return line

    def _getDigestStartPos(self, line, mode):
        """
        return the start position of the digest returned by _getDigest()
        Args:
            mode: 0, 1, 2, return 1
        """
        return 0

    def _createHelp(self):
        help = []
        help.append('" i : switch to input mode')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append('" <CR> : accept')
        help.append('" ---------------------------------------------------------')
        return help

    def _afterEnter(self):
        super(CppIncludeExplManager, self)._afterEnter()

    def _beforeExit(self):
        super(CppIncludeExplManager, self)._beforeExit()


cppIncludeExplManager = CppIncludeExplManager()

__all__ = ['cppIncludeExplManager']
