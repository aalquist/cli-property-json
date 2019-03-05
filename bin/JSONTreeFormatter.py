import os
import re

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

    #def escapeSpecialCharacters (self, text, characters ):
    #    for character in characters:
    #        text = text.replace( character, '\\' + character )
    #    return text

    def printJsonPointer(self,json, path):

            if( isinstance(json, list)):

                print(os.linesep)
                for i in range(0,len(json)):

                    subjson = json[i]
                    if isinstance(json[i], dict) and "name" in subjson:
                        print("{}/{} > name={}".format(path,i, subjson["name"]) )

                    else:
                        print("{}/{}".format(path,i) )
            else: 
                
                if isinstance(json, dict) and "name" in json:
                        print("{} > name={}".format(path, json["name"] ) )


                else:
                    print("{}".format(path) )

