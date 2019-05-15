import os
import re

from . import JSONTraversalTools


class JSONTreeFormatter():

    def jsonPathtoJsonPointer(self, jsonPath):

        

        #(?P<name>
        regex = r"(\.\[(?P<name>\d+)\](\.)?)"
        subst = "*\g<name>*"
        result = re.sub(regex, subst, jsonPath, 0, re.MULTILINE)

        regex2 = r"(\*|\.)"   
        subst2 = "/"
        result = re.sub(regex2, subst2, result, 0, re.MULTILINE) 
        
        regex3 = r"^(\$)"   
        subst3 = ""
        result = re.sub(regex3, subst3, result, 0, re.MULTILINE) 

        regex3 = r"\/$"   
        subst3 = ""
        result = re.sub(regex3, subst3, result, 0, re.MULTILINE) 

        return result

    def getTreeSummary(self, originalJsonPath, originalJsonRuleTree, returnEmpty = True, printPointers = True):

        tools = JSONTraversalTools.JSONTraversalTools()

        pathResultArray = tools.resolveJsonPathstoPointers(originalJsonRuleTree, originalJsonPath)    
    
        if originalJsonPath :
            print(originalJsonPath) 

        output = []
        for pathPair in pathResultArray:
            
            jsonPathPair = pathPair[0]
            jsonPointerPair = pathPair[1]
            

            if printPointers:
                resolved = tools.resolveJsonPointer(originalJsonRuleTree,jsonPointerPair)
                path = jsonPointerPair
            else:
                resolved = tools.resolveJsonPaths(originalJsonRuleTree,jsonPathPair)[1]
                path = jsonPathPair

            
            result = self.printJsonPointer(resolved, path, "", returnEmpty)
            
            if result is not None:
                output.append( result )

        

        maxpathchars = 0
        for o in output: 
            left = o.split("\t")
            size = len(left[0]) + 1
            if maxpathchars < size:
                maxpathchars = size

            

        for o in output:    
            print(o.expandtabs(maxpathchars))

    def printJsonPointer(self,json, path, indent = "", returnEmpty = False, returnKeys = False ):

            
            if( isinstance(json, list)):

                if len(json) > 0:
                    for i in range(0,len(json)):

                        subjson = json[i]
                        if isinstance(json[i], dict) and "name" in subjson:
                            
                            if returnKeys :
                                keys = list(json.keys() )
                                keys.remove("name")
                                return ("{}{}/{} \t name={}\t {}".format(indent,path,i, subjson["name"], keys) )
                            else : 
                                return ("{}{}/{} \t name={}".format(indent,path,i, subjson["name"]) )

                            

                        else:
                            return ("{}{}/{}".format(indent,path,i) )
                elif returnEmpty == False:
                    return ("{}{}\t[]".format(indent,path) )
                else: 
                    return None
            else: 
                
                if isinstance(json, dict) and "name" in json:
                        
                        if returnKeys :
                            keys = list(json.keys() )
                            keys.remove("name")
                            return ("{}{} \t name={}\t {}".format(indent,path, json["name"], keys ) )
                        else : 
                            return ("{}{} \t name={}".format(indent,path, json["name"] ) )


                else:
                    return ("{}{}".format(indent,path) )

           