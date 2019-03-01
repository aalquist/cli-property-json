import os

class JSONTreeFormatter():

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

