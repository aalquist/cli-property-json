import jsonpointer
from jsonpath_ng import jsonpath, parse
import os
import copy
from .JSONTreeFormatter import JSONTreeFormatter

class JSONTraversalTools():

    def appendToArray(self, doc, path, fragment):
        doc = copy.deepcopy(doc)
        siblingJson = jsonpointer.resolve_pointer(doc, path)
        siblingJson.append(fragment)
        return jsonpointer.set_pointer(doc, path,siblingJson, inplace=False)

    def prependToArray(self, doc, path, fragment):
        doc = copy.deepcopy(doc)
        siblingJson = jsonpointer.resolve_pointer(doc, path)
        siblingJson.insert(0,fragment)
        return jsonpointer.set_pointer(doc, path,siblingJson, inplace=False)
        
    def getJsonPaths(self, doc, jsonPath):
        returnArray = []
        for match in parse(jsonPath).find(doc):
            m = str(match.full_path)
            returnArray.append(m)    
        return returnArray

    def resolveJsonPaths(self, doc, jsonPath):
        returnArray = []
        for match in parse(jsonPath).find(doc):
            returnArray.extend((str(match.full_path), match.value) )
        return returnArray

    def resolveJsonPathstoPointers(self, doc, jsonPath):
        formatter = JSONTreeFormatter()
        returnArray = []

        pathArray = self.getJsonPaths(doc, jsonPath)

        for jsonPath in pathArray:
            
            pathValues = self.resolveJsonPaths(doc, jsonPath)
            subpath = pathValues[0]
            subjson = pathValues[1]
            isList = isinstance(subjson, list)
            isElement = all( not isinstance(elem, list) and not isinstance(elem, dict) for elem in subjson)  

            if not isElement and isList and len(subjson) > 0: #skip jsonPaths that won't resolve to a single object

                #testing jsonPoninter and jsonPaths are returning equal values
                for i in range(0,len(subjson)): 
                    updatedPath = "{}.[{}]".format(subpath,i)
                    pointer = "/{}".format(formatter.jsonPathtoJsonPointer(updatedPath))
                    returnArray.append( (updatedPath, pointer) ) 
            else:
                pointer = "/{}".format(formatter.jsonPathtoJsonPointer(subpath))
                returnArray.append( (subpath, pointer) ) 

        returnArray.sort()

        return returnArray

    def resolveJsonPointer(self, doc, jsonPointer):
        returnJson = jsonpointer.resolve_pointer(doc, jsonPointer)
        return returnJson

    def fetchPointer(self, doc, path):

        #TODO Bad Pointer Handeling
        jsonObj = jsonpointer.resolve_pointer(doc, path)
        return jsonObj
    
    def getJsonPointerArray(self,json, path):

        returnList = []

        if( isinstance(json, list)):

            for i in range(0,len(json)):
                
                subjson = json[i]
                returnMap = {} 

                if isinstance(json[i], dict) and "name" in subjson:
                    returnMap["name"] = subjson["name"]
                    returnMap["path"] = "{}/{}".format(path,i)
                    returnMap["_keys"] = list(subjson.keys())

                elif isinstance(json[i], dict):
                    returnMap["_keys"] = list(subjson.keys())

                else:
                    returnMap["path"] = "{}/{}".format(path,i)
                    returnMap["_value"] = json[i]

                returnMap["_value"] = subjson

                returnList.append(returnMap)

            return returnList
                    
        else: 

            returnMap = {} 

            if isinstance(json, dict) and "name" in json:

                returnMap["name"] = json["name"]
                returnMap["path"] = path
                returnMap["_value"] = json
            
            else:
                returnMap["path"] = path
                returnMap["_value"] = json

            if isinstance(json, dict):

                returnMap["_keys"] = list(json.keys())
    
            
            returnList.append(returnMap)
            return returnList
