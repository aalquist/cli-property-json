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
import json
import jsonpointer
import sys

from jsonpath_ng import jsonpath, parse

from bin.JSONTraversalTools import JSONTraversalTools
from bin.JSONTreeFormatter import JSONTreeFormatter

class Property_JSON_Tests(unittest.TestCase):

    basedir = os.path.abspath(os.path.dirname(__file__))

    def testInjectPointer(self):
        tools = JSONTraversalTools()
        doc = self.getJSONFromFile( "{}/json/ruletrees/new-ion-standard.rule-tree.json".format( self.basedir ) )
        
        path = '/rules/children'
        resultArray = tools.fetchPointer(doc, path)
        self.assertEqual(2, len(resultArray) )
        self.assertEqual("Performance", resultArray[0]["name"])
        self.assertEqual("Offload", resultArray[1]["name"])

        jsonTreeFragment = self.getJSONFromFile( "{}/json/fragments/cache-pages.json".format( self.basedir ) )
        modifiedJson = tools.appendToArray(doc, path, jsonTreeFragment)

        pointerContent = tools.fetchPointer(modifiedJson, path)
        self.assertEqual(3, len(pointerContent) )

        resultArray = tools.getJsonPointerArray(pointerContent, path)
        self.assertEqual("Performance", resultArray[0]["name"])
        self.assertEqual("Offload", resultArray[1]["name"])
        self.assertEqual("Cache Pages", resultArray[2]["name"])

        modifiedJson = tools.prependToArray(doc, path, jsonTreeFragment)

        pointerContent = tools.fetchPointer(modifiedJson, path)
        self.assertEqual(3, len(pointerContent) )

        resultArray = tools.getJsonPointerArray(pointerContent, path)
        self.assertEqual("Cache Pages", resultArray[0]["name"])
        self.assertEqual("Performance", resultArray[1]["name"])
        self.assertEqual("Offload", resultArray[2]["name"])
        

    def testFetchPointer(self):
        tools = JSONTraversalTools()
        doc = self.getJSONFromFile( "{}/json/ruletrees/new-ion-standard.rule-tree.json".format( self.basedir ) )
        
        path = '/rules/children'
        pointerContent = tools.fetchPointer(doc, path)
        resultArray = tools.getJsonPointerArray(pointerContent, path)

        self.assertEqual(2, len(resultArray) )
        self.assertEqual("Performance", resultArray[0]["name"])
        self.assertEqual("Offload", resultArray[1]["name"])

        self.assertIn("criteria", resultArray[1]["_keys"])
        self.assertIn("criteriaMustSatisfy", resultArray[1]["_keys"])
        self.assertIn("comments", resultArray[1]["_keys"])
        self.assertIn("name", resultArray[1]["_keys"])
        self.assertIn("behaviors", resultArray[1]["_keys"])
        self.assertIn("children", resultArray[1]["_keys"])

        path = '/rules/children/0'
        pointerContent = tools.fetchPointer(doc, path)
        resultArray = tools.getJsonPointerArray(pointerContent, path)
        self.assertEqual(1, len(resultArray) )
        self.assertEqual("Performance", resultArray[0]["name"])
        
        self.assertEqual(6, len(resultArray[0]["_keys"]) )
        self.assertIn("criteria", resultArray[0]["_keys"])
        self.assertIn("criteriaMustSatisfy", resultArray[0]["_keys"])
        self.assertIn("comments", resultArray[0]["_keys"])
        self.assertIn("name", resultArray[0]["_keys"])
        self.assertIn("behaviors", resultArray[0]["_keys"])
        self.assertIn("children", resultArray[0]["_keys"])

        path = '/rules/children/0/children/0/behaviors/0/options'
        pointerContent = tools.fetchPointer(doc, path)
        resultArray = tools.getJsonPointerArray(pointerContent, path)
        self.assertEqual(1, len(resultArray) )
        self.assertEqual("ALWAYS", resultArray[0]["_value"]["behavior"])

        path = '/rules/children/0/children/0/criteria/0/options/values'
        pointerContent = tools.fetchPointer(doc, path)
        resultArray = tools.getJsonPointerArray(pointerContent, path)
        self.assertEqual(21, len(resultArray) )
        self.assertEqual("text/*", resultArray[0]["_value"])
        self.assertEqual("image/vnd.microsoft.icon", resultArray[20]["_value"])
        
        path = '/rules/children/1'
        pointerContent = tools.fetchPointer(doc, path)
        resultArray = tools.getJsonPointerArray(pointerContent, path)
        self.assertEqual(1, len(resultArray) )
        self.assertEqual("Offload", resultArray[0]["name"])

        self.assertEqual(6, len(resultArray[0]["_keys"]) )
        self.assertIn("criteria", resultArray[0]["_keys"])
        self.assertIn("criteriaMustSatisfy", resultArray[0]["_keys"])
        self.assertIn("comments", resultArray[0]["_keys"])
        self.assertIn("name", resultArray[0]["_keys"])
        self.assertIn("behaviors", resultArray[0]["_keys"])
        self.assertIn("children", resultArray[0]["_keys"])

        path = '/ruleFormat'
        pointerContent = tools.fetchPointer(doc, path)
        resultArray = tools.getJsonPointerArray(pointerContent, path)
        self.assertEqual(1, len(resultArray) )
        self.assertEqual("latest", resultArray[0]["_value"])



    def testJSONPathtoJSONPointer(self):

        formatter = JSONTreeFormatter()
        
        result = formatter.jsonPathtoJsonPointer("$.rules.children.[0].children.[0]")
        self.assertEqual("/rules/children/0/children/0", result )

        result = formatter.jsonPathtoJsonPointer("$.rules.children.[0].children")
        self.assertEqual("/rules/children/0/children", result )

        result = formatter.jsonPathtoJsonPointer(".rules.children.[0].children")
        self.assertEqual("/rules/children/0/children", result )

        result = formatter.jsonPathtoJsonPointer(".rules.children")
        self.assertEqual("/rules/children", result )

        result = formatter.jsonPathtoJsonPointer(".rules.children.[0].children")
        self.assertEqual("/rules/children/0/children", result )

        result = formatter.jsonPathtoJsonPointer(".rules.children.[0].children.[0].children")
        self.assertEqual("/rules/children/0/children/0/children", result )

        result = formatter.jsonPathtoJsonPointer(".rules.children.[1].children")
        self.assertEqual("/rules/children/1/children", result )

        result = formatter.jsonPathtoJsonPointer(".rules.children.[1].children.[01].children")
        self.assertEqual("/rules/children/1/children/01/children", result )

        result = formatter.jsonPathtoJsonPointer(".rules.children.[1].children.[10].children")
        self.assertEqual("/rules/children/1/children/10/children", result )

        result = formatter.jsonPathtoJsonPointer(".rules.children.[1].children.[200].children")        
        self.assertEqual("/rules/children/1/children/200/children", result )


    def testJSON_Taversals(self):

        basedir = os.path.abspath(os.path.dirname(__file__))
        originalJsonRuleTree = self.getJSONFromFile( "{}/json/ruletrees/new-ion-standard.rule-tree.json".format( basedir ) )
        
        tools = JSONTraversalTools()
        formatter = JSONTreeFormatter()

        someArray = tools.resolveJsonPathstoPointers(originalJsonRuleTree, "$..children")
        self.assertEqual(10,len(someArray ))

        for pathPair in someArray:
            jsonPathPair = pathPair[0]
            jsonPointerPair = pathPair[1]

            resolvedJsonPointer = tools.resolveJsonPointer(originalJsonRuleTree,jsonPointerPair)
            resolvedJsonPath = tools.resolveJsonPaths(originalJsonRuleTree,jsonPathPair)
            self.assertEqual(resolvedJsonPointer,resolvedJsonPath[1])
            

        
        
    def getJSONFromFile(self, jsonPath):
        
        with open(jsonPath, 'r') as myfile:
            jsonStr = myfile.read()
        
        jsonObj = json.loads(jsonStr)
        return jsonObj
   

if __name__ == '__main__':
    unittest.main()



