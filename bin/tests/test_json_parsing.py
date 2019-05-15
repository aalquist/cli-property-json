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
from io import StringIO

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

    def testAll(self):

        listOfStrings = [ "abc", "123", "xyz"]

        result = all( not isinstance(elem, list) and not isinstance(elem, dict) for elem in listOfStrings)    

        self.assertTrue(result)

    def testJSON_Summary(self):

        basedir = os.path.abspath(os.path.dirname(__file__))
        originalJsonRuleTree = self.getJSONFromFile( "{}/json/ruletrees/new-ion-standard.rule-tree.json".format( basedir ) )
        
        originalJsonPath = "$..children"

        formatter = JSONTreeFormatter()
        
        result = self.redirectOutputToArray(lambda originalJsonPath : formatter.getTreeSummary(originalJsonPath, originalJsonRuleTree) , originalJsonPath, True)
        self.assertEqual(7, len(result) )
        
        self.assertEqual(originalJsonPath, result[0])
        self.assertEqual("/rules/children/0              name=Performance", result[1])
        self.assertEqual("/rules/children/0/children/0   name=Compressible Objects", result[2])
        self.assertEqual("/rules/children/1              name=Offload", result[3])
        self.assertEqual("/rules/children/1/children/0   name=CSS and JavaScript", result[4])
        self.assertEqual("/rules/children/1/children/1   name=Static Objects", result[5])
        self.assertEqual("/rules/children/1/children/2   name=Uncacheable Responses", result[6])
        

        result = self.redirectOutputToArray(lambda originalJsonPath : formatter.getTreeSummary(originalJsonPath, originalJsonRuleTree, True, False) , originalJsonPath, True)
        self.assertEqual(7, len(result) )

        self.assertEqual(originalJsonPath, result[0])
        self.assertEqual("rules.children.[0]                name=Performance", result[1])
        self.assertEqual("rules.children.[0].children.[0]   name=Compressible Objects", result[2])
        self.assertEqual("rules.children.[1]                name=Offload", result[3])
        self.assertEqual("rules.children.[1].children.[0]   name=CSS and JavaScript", result[4])
        self.assertEqual("rules.children.[1].children.[1]   name=Static Objects", result[5])
        self.assertEqual("rules.children.[1].children.[2]   name=Uncacheable Responses", result[6])
        
        result = self.redirectOutputToArray(lambda originalJsonPath : formatter.getTreeSummary(originalJsonPath, originalJsonRuleTree, False) , originalJsonPath, True)
        self.assertEqual(11, len(result) )
        self.assertEqual(originalJsonPath, result[0])
        self.assertEqual("/rules/children/0                      name=Performance", result[1])
        self.assertEqual("/rules/children/0/children/0           name=Compressible Objects", result[2])
        self.assertEqual("/rules/children/0/children/0/children []", result[3])
        self.assertEqual("/rules/children/1                      name=Offload", result[4])
        self.assertEqual("/rules/children/1/children/0           name=CSS and JavaScript", result[5])
        self.assertEqual("/rules/children/1/children/0/children []", result[6])
        self.assertEqual("/rules/children/1/children/1           name=Static Objects", result[7])
        self.assertEqual("/rules/children/1/children/1/children []", result[8])
        self.assertEqual("/rules/children/1/children/2           name=Uncacheable Responses", result[9])
        self.assertEqual("/rules/children/1/children/2/children []", result[10])
    


        originalJsonPath = "rules.children.[0]"
        result = self.redirectOutputToArray(lambda originalJsonPath : formatter.getTreeSummary(originalJsonPath, originalJsonRuleTree, True, False) , originalJsonPath, True)
        self.assertEqual(2, len(result) )
        self.assertEqual(originalJsonPath, result[0])
        self.assertEqual("rules.children.[0]   name=Performance", result[1])

        originalJsonPath = "rules.children[0]"
        result = self.redirectOutputToArray(lambda originalJsonPath : formatter.getTreeSummary(originalJsonPath, originalJsonRuleTree, True, False) , originalJsonPath, True)
        self.assertEqual(2, len(result) )
        self.assertEqual(originalJsonPath, result[0])
        self.assertEqual("rules.children.[0]   name=Performance", result[1])

        originalJsonPath = "$..criteria"
        result = self.redirectOutputToArray(lambda originalJsonPath : formatter.getTreeSummary(originalJsonPath, originalJsonRuleTree, True, False) , originalJsonPath, True)
        self.assertEqual(5, len(result) )
        self.assertEqual(originalJsonPath, result[0])
        self.assertEqual("rules.children.[0].children.[0].criteria.[0]   name=contentType", result[1])
        self.assertEqual("rules.children.[1].children.[0].criteria.[0]   name=fileExtension", result[2])
        self.assertEqual("rules.children.[1].children.[1].criteria.[0]   name=fileExtension", result[3])
        self.assertEqual("rules.children.[1].children.[2].criteria.[0]   name=cacheability", result[4]) 


        originalJsonPath = "rules.children.[1].children.[0].criteria.[0]"
        result = self.redirectOutputToArray(lambda originalJsonPath : formatter.getTreeSummary(originalJsonPath, originalJsonRuleTree, True, False) , originalJsonPath, True)
        self.assertEqual(2, len(result) )
        self.assertEqual(originalJsonPath, result[0])
        self.assertEqual("rules.children.[1].children.[0].criteria.[0]   name=fileExtension", result[1])


        originalJsonPath = "rules.children.[1].children.[1].criteria.[0].options.values"
        result = self.redirectOutputToArray(lambda originalJsonPath : formatter.getTreeSummary(originalJsonPath, originalJsonRuleTree, True) , originalJsonPath, True)
        
        self.assertEqual(2, len(result) )
        self.assertEqual(originalJsonPath, result[0])
        self.assertEqual("/rules/children/1/children/1/criteria/0/options/values/0", result[1])

        originalJsonPath = "$..*"
        result = self.redirectOutputToArray(lambda originalJsonPath : formatter.getTreeSummary(originalJsonPath, originalJsonRuleTree, True) , originalJsonPath, True)
        
        self.assertEqual(179, len(result) )
        self.assertEqual(originalJsonPath, result[0])

        self.assertEqual('/accountId', result[1])
        self.assertEqual('/contractId', result[2])
        #skipping some tests
        self.assertEqual('/rules                                                              name=default', result[8])
        self.assertEqual('/rules/behaviors/0                                                  name=origin', result[9])
        #skipping more tests
        self.assertEqual('/rules/options/is_secure', result[178])
        

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

    def testJSON_Taversals(self):

        basedir = os.path.abspath(os.path.dirname(__file__))
        originalJsonRuleTree = self.getJSONFromFile( "{}/json/ruletrees/new-ion-standard.rule-tree.json".format( basedir ) )
        
        tools = JSONTraversalTools()
        formatter = JSONTreeFormatter()

        originalJsonPath = "$..children"
        someArray = tools.resolveJsonPathstoPointers(originalJsonRuleTree, originalJsonPath)
        self.assertEqual(10,len(someArray ))

        output = []
        for pathPair in someArray:
            jsonPathPair = pathPair[0]
            jsonPointerPair = pathPair[1]

            resolvedJsonPointer = tools.resolveJsonPointer(originalJsonRuleTree,jsonPointerPair)
            resolvedJsonPath = tools.resolveJsonPaths(originalJsonRuleTree,jsonPathPair)[1]
    
            self.assertEqual(resolvedJsonPointer,resolvedJsonPath)

            
            result = formatter.printJsonPointer(resolvedJsonPointer, jsonPointerPair)
            self.assertIsNotNone(result)

            result = formatter.printJsonPointer(resolvedJsonPointer, jsonPointerPair, "", True)
            output.append(result)

       

        self.assertIn(None, output)


        
        
    def getJSONFromFile(self, jsonPath):
        
        with open(jsonPath, 'r') as myfile:
            jsonStr = myfile.read()
        
        jsonObj = json.loads(jsonStr)
        return jsonObj
   

if __name__ == '__main__':
    unittest.main()



