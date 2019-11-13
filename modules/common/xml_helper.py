from xml.etree import ElementTree
from xml.dom import minidom


def pretify(elem):
    string = ElementTree.tostring(elem, 'utf-8')
    string = string.decode().replace("\n", "").replace("\t", "").encode()
    reparsed = minidom.parseString(string)
    return reparsed.toprettyxml(indent="\t")


def read_xml(path):
    return ElementTree.parse(path)


def write_xml(path, xml_data):
    with open(path, 'w') as file:
        file.write(pretify(xml_data))


def add_element_to_root(xml_data, tag, text):
    root = xml_data.getroot()
    new = ElementTree.SubElement(root, tag)
    new.text = text
    return root