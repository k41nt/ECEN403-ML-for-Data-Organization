"""
Title:: XML extractor
Brief:: A simple program that extracts values from xml file
Author:: Khanh Nguyen
Date:: 04/02/2019
"""
import xml.etree.ElementTree as ET
import json
import os

#This function parses child nodes under root node
def parse_node(node, ancestor_string=""):
    if ancestor_string:
        node_string = ".".join([ancestor_string, node.tag])
    else:
        node_string = node.tag
    text = node.text
    if text:
        text_list = [text.strip()]
    else:
        text_list = [""]
    for child_node in list(node):
        child_text_list= parse_node(child_node, ancestor_string=node_string)
        text_list.extend(child_text_list)
    return text_list

#This function parses the whole xml and put keywords into a json
def xml_extractor(path):
    tree = ET.parse(path)
    root_node = tree.getroot()
    text= parse_node(root_node)
    text = list(filter(None, text)) #filter empty strings
    text_dict = list( dict.fromkeys(text) ) #convert list to dictionary and remove dupplicates
    with open((path[:-3])+'json', 'w') as file_out:
        json.dump(text_dict, file_out, indent=4)

# Main    
if __name__ == '__main__':
    #list to hold all the file names
    file_list = []

    #iterate through the path to get all pdf files
    for path, subdirs, files in os.walk(os.path.realpath(__file__)): # change this path to current working folder
        for filename in files:
            if '.xml' in filename:
                    file_list.append(filename)
    
    #convert and extract each file in file_list
    for file in file_list:
        xml_extractor(file)