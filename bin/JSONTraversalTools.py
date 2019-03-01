import jsonpointer
import os
import copy

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
