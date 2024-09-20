
import csv
import json
import sys

import logging
import re


class RegisterMapperHFile():

    def __init__(self, file_path, out_file, reg_name_prefix="(\w*)_C_REG_([A-Z]+)_(\w+)_[ABE]"):
        logging.debug("Reading registers from %s", file_path)
        self.json_dict = {}
        with open(file_path, "r") as file:
            map = ""
            reg = ""

            map_dict_pos = None

            for row in file:
                row = row.split("//", 1)[0]

                parts = row.split()
                parts = list(filter(None, parts))

                #skip parts[0] as it will just be #define
                name = parts[1]
                addr = int(parts[2], 0)

                x = re.search(reg_name_prefix, name)

                if name.endswith("_A"):
                    
                    map_with_num = x.group(1)
                    map = x.group(2)
                    reg = x.group(3)

                    if map not in self.json_dict:
                        self.json_dict[map] = {}
                        map_dict_pos = self.json_dict[map]
                    
                    if map_with_num[-1] != "0" and map_with_num[-1] not in self.json_dict[map]:
                        self.json_dict[map][map_with_num[-1]] = {}
                        map_dict_pos = self.json_dict[map][map_with_num[-1]]
                    
                    map_dict_pos[reg] = {}
                    map_dict_pos[reg]["addr"] = addr
                    map_dict_pos[reg]["size"] = 4
                    map_dict_pos[reg]["readonly"] = "STATUS" in reg

                elif name.endswith("_B"):
                    field = x.group(3)

                    if field.startswith(reg):
                        # removes the prefix
                        field = field[len(reg + "_"):]
                        if "fields" not in map_dict_pos[reg]:
                           map_dict_pos[reg]["fields"] = {}
                        
                        map_dict_pos[reg]["fields"][field] = addr

                    else:
                        # field is marked as belonging to a different register, find it
                        logging.debug("Searching for register for field %s", field)
                        for exist_reg in map_dict_pos:
                            if field.startswith(exist_reg):
                                field = field[len(exist_reg + "_"):]
                                if "fields" not in map_dict_pos[exist_reg]:
                                    map_dict_pos[exist_reg]['fields'] = {}
                                
                                map_dict_pos[exist_reg]['fields'][field] = addr
                elif name.endswith("_E"):
                    pass # we're ignoring enum definitions for now

        with open(out_file, "w") as outfile:
            json.dump(self.json_dict, outfile, indent=2)
            logging.debug("File Output to %s. Remember to go in and edit sizes of registers and fields",
                          out_file)




if __name__ == "__main__":
    print("Reading h File: ")

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)

    input = sys.argv[1]
    output = sys.argv[2]

    mapper = RegisterMapperHFile(input, output)
