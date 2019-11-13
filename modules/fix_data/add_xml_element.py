from xml.etree import ElementTree
from xml.dom import minidom

def pretify(elem):
    string = ElementTree.tostring(elem, 'utf-8')
    string = string.decode().replace("\n","").replace("\t","").encode()
    reparsed = minidom.parseString(string)
    return reparsed.toprettyxml(indent="\t")

xml_data = ElementTree.parse("../../data/2847267.xml")
root = xml_data.getroot()
new = ElementTree.SubElement(root,"ClassId")
new.text = "abc"

with open("tesst.xml", 'w') as file:
    file.write(pretify(root))
debug = 1