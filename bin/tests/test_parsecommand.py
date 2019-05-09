

# Copyright 2017 Akamai Technologies, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import os
import sys
from bin.parsecmd import main  as parsecmd_main

class ParseCmdTest(unittest.TestCase):

    def test_main(self):

        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "{}/json/ruletrees/new-ion-standard.rule-tree.json".format( basedir )

        args = [
                "parseTree",
                "--file",
                path,
                "--jsonpath",
                "$..criteria"
            ]

        parsecmd_main(args)

        args = [
                "getpointer",
                "--show-json",
                "--file",
                path,
                "--jsonpointer",
                "/rules/children"
                
            ]
        parsecmd_main(args)

        args = [ "help"]
        parsecmd_main(args)

        args = [ "help", "getpointer"]
        parsecmd_main(args)

        #parsecmd_main(None)
        parsecmd_main([])

        #print(sys.argv)

        
       

if __name__ == '__main__':
    unittest.main()


