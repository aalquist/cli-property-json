#!/usr/bin/env python3

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

import argparse
import sys
import os
import inspect


from bin.JSONTraversalTools import JSONTraversalTools
from bin.JSONTreeFormatter import JSONTreeFormatter

import json

PACKAGE_VERSION = "0.0.1"

class MyArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(0, '%s: error: %s\n' % (self.prog, message))

def get_prog_name():
    prog = os.path.basename(sys.argv[0])
    if os.getenv("AKAMAI_CLI"):
        prog = "akamai property-json"
    return prog

def create_sub_command( subparsers, name, help, *, optional_arguments=None, required_arguments=None):

    action = subparsers.add_parser(name=name, help=help, add_help=False)

    if required_arguments:
        required = action.add_argument_group("required arguments")
        for arg in required_arguments:
            name = arg["name"]
            del arg["name"]
            required.add_argument("--" + name,
                                  required=True,
                                  **arg)

    optional = action.add_argument_group("optional arguments")

    if optional_arguments:
        for arg in optional_arguments:
            name = arg["name"]
            del arg["name"]

            

            if name.startswith("use-") or name.startswith("show-"):
                optional.add_argument(
                    "--" + name,
                    required=False,
                    **arg,
                    action="store_true")
            else:
                optional.add_argument("--" + name,
                                      required=False,
                                      **arg)

    optional.add_argument(
        "--edgerc",
        help="Location of the credentials file [$AKAMAI_EDGERC]",
        default=os.path.join(os.path.expanduser("~"), '.edgerc'))

    optional.add_argument(
        "--section",
        help="Section of the credentials file [$AKAMAI_EDGERC_SECTION]",
        default="default")

    optional.add_argument(
        "--debug",
        help="DEBUG mode to generate additional logs for troubleshooting",
        action="store_true")

    optional.add_argument(
        "--account-key",
        help="Account Switch Key",
        default="")

    return action

def main(mainArgs=None):

    prog = get_prog_name()
    if len(sys.argv) == 1:
        prog += " [command]"

    parser = MyArgumentParser(
            description='Akamai Property Manager JSON Parser',
            add_help=False,
            prog=prog
    )

    parser.add_argument('--version', action='version', version='%(prog)s ' + PACKAGE_VERSION)

    subparsers = parser.add_subparsers(help='commands', dest="command")

    actions = {}

    subparsers.add_parser(
        name="help",
        help="Show available help",
        add_help=False).add_argument( 'args', metavar="", nargs=argparse.REMAINDER)

    actions["showpaths"] = create_sub_command(
        subparsers, "showpaths", "Display and navigate Property Manager JSON file in easier to read format",
        optional_arguments=[
                            {"name": "file", "help": "the JSON file to parse"}, 
                            {"name": "jsonpath", "help": "jsonpath string to print summary"},
                            {"name": "use-stdin", "help": "use stdin as input"} ],
        required_arguments=None)
    
    actions["getpointer"] = create_sub_command(
        subparsers, "getpointer", "Display and navigate Property Manager JSON file in easier to read format",
        optional_arguments=[
                            {"name": "file", "help": "the file as input"}, 
                            {"name": "jsonpointer", "help": "jsonpointer string to print json"},
                            {"name": "show-json", "help": "display json output"},
                            {"name": "use-stdin", "help": "use stdin as input"} ],
        required_arguments=None)

    args = None

    if mainArgs is None: 
        parser.print_help()
        return 1

    elif isinstance(mainArgs, list) and len(mainArgs) <= 0: 
        parser.print_help()
        return 1

    else:
        args = parser.parse_args(mainArgs)



    if args.command == "help":

        if len(args.args) > 0:
            if actions[args.args[0]]:
                actions[args.args[0]].print_help()
        else:
            parser.prog = get_prog_name() + " help [command]"
            parser.print_help()
            

        return 0

    try:
        return getattr(sys.modules[__name__], args.command.replace("-", "_"))(args)

    except Exception as e:
        print(e, file=sys.stderr)
        return 1

def getJSONFromSTDIN():
        
        with open(0, 'r') as myfile:
            jsonStr = myfile.read()
        
        jsonObj = json.loads(jsonStr)
        return jsonObj

def getJSONFromFile(jsonPath):
        
        with open(jsonPath, 'r') as myfile:
            jsonStr = myfile.read()
        
        jsonObj = json.loads(jsonStr)
        return jsonObj

def showpaths(args):

    if(args.use_stdin or args.file is None):
        originalJsonRuleTree = getJSONFromSTDIN()

    else:
        originalJsonRuleTree = getJSONFromFile( args.file )

    originalJsonPath = args.jsonpath

    formatter = JSONTreeFormatter()
    formatter.getTreeSummary(originalJsonPath, originalJsonRuleTree)
    return 0

def getpointer(args):

    if(args.use_stdin):
        originalJsonRuleTree = getJSONFromSTDIN()
    else:    
        originalJsonRuleTree = getJSONFromFile( args.file )

    pointer = args.jsonpointer

    tools = JSONTraversalTools()
    pointerContent = tools.fetchPointer(originalJsonRuleTree, pointer)

    if args.show_json:
        print(json.dumps( pointerContent) )
        
    return 0
