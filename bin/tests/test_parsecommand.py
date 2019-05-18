

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
import json
from io import StringIO

from bin.parsecmd import main  as parsecmd_main

class ParseCmdTest(unittest.TestCase):

    def test_main(self):

        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "{}/json/ruletrees/new-ion-standard.rule-tree.json".format( basedir )

        args = [
                "showpaths",
                "--file",
                path,
                "--jsonpath",
                "$..criteria"
            ]
        #print("\n###testing args: {}".format(args))
        result = self.redirectOutputToArray(lambda args : parsecmd_main(args) , args, True)
        self.assertEqual(5, len(result) )

        self.assertEqual("$..criteria", result[0])
        self.assertEqual("/rules/children/0/children/0/criteria/0   name=contentType", result[1])
        self.assertEqual("/rules/children/1/children/0/criteria/0   name=fileExtension", result[2])
        self.assertEqual("/rules/children/1/children/1/criteria/0   name=fileExtension", result[3])
        self.assertEqual("/rules/children/1/children/2/criteria/0   name=cacheability", result[4]) 
        

        args = [
                "getpointer",
                "--show-json",
                "--file",
                path,
                "--jsonpointer",
                "/rules/children"
                
            ]
        
        #print("\n###testing args: {}".format(args))
        result = self.redirectOutputToArray(lambda args : parsecmd_main(args) , args, False)
        self.assertEqual(2, len(result) )
        jsondict = json.loads( result[0] )
        self.assertEqual(2, len(jsondict) )

        args = [ "help"]
        #print("\n###testing args: {}".format(args))
        result = self.redirectOutputToArray(lambda args : parsecmd_main(args) , args, False)
        self.assertTrue(len(result) > 0 )

        
        args = [ "help", "getpointer"]
        #print("\n###testing args: {}".format(args))
        result = self.redirectOutputToArray(lambda args : parsecmd_main(args) , args, False)
        self.assertTrue(len(result) > 0 )


    def redirectOutputToArray(self, fun, value, ignoreNewLines = True):

        saved_stdout = sys.stdout
        
        out = StringIO()
        sys.stdout = out
        
        fun(value)

        output = list(out.getvalue().split("\n"))
        
        if ignoreNewLines:
            output = list(filter(lambda line: line != '', output))

        
        sys.stdout = saved_stdout

        return output
       

if __name__ == '__main__':
    unittest.main()


