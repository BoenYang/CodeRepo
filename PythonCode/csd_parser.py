# coding:utf-8

import xml.dom.minidom as minidom
from xml.dom import Node
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def copy_child_attrs(src_element, dst_element, exclude = []):
    children1 = src_element.childNodes
    children2 = dst_element.childNodes
    for i in range(0, len(children1)):
        child1 = children1[i]
        child2 = children2[i]
        if child1.nodeType != Node.TEXT_NODE and child1.nodeName == 'Children' and child1 not in exclude:
            print child1.nodeName
            for key in child1.attributes.keys():
                attr1 = child1.attributes[key]
                if child2.hasAttribute(key):
                    attr2 = child2.attributes[key]
                    attr2.value = attr1.value
                else:
                    child2.setAttribute(key, attr1.value)


def copy_child_attrs_by_arr(src_element, dst_element, attrs):
    children1 = src_element.childNodes
    children2 = dst_element.childNodes
    for i in range(0, len(children1)):
        child1 = children1[i]
        child2 = children2[i]
        if child1.nodeType != Node.TEXT_NODE and child1.nodeName != 'Children' and child1.nodeName in attrs:
            print child1.nodeName
            for key in child1.attributes.keys():
                attr1 = child1.attributes[key]
                if child2.hasAttribute(key):
                    attr2 = child2.attributes[key]
                    attr2.value = attr1.value
                    print attr1.value
                else:
                    child2.setAttribute(key, attr1.value)
                    print attr1.value


def get_node_by_name(node, name):
    _nodes = node.getElementsByTagName('AbstractNodeData')
    for n in _nodes:
        _name = n.getAttribute('Name')
        if _name == name:
            return n


def get_node_by_pattern(nodes, name_pattern):
    node_arr = []
    for n in nodes:
        _name = n.getAttribute('Name')
        if re.match(name_pattern, _name):
            node_arr.append(n)
    return node_arr


if __name__ == '__main__':
    xml_file = 'Z:\\workspace\\jdi\\d05_code_dev\\cocosstudio_sgw\\cocosstudio\\files\\sgw\\roomMandate.csd'
    dom = minidom.parse(xml_file)
    dom_root = dom.documentElement
    nodes = dom_root.getElementsByTagName('AbstractNodeData')

    radio_template = get_node_by_pattern(nodes, 'radioBtn')[0]
    pull_down_panel_template = get_node_by_pattern(nodes, 'pulldown')[0]
    pull_down_btn_template = get_node_by_pattern(nodes, 'pulldownBtn')[0]
    help_btn_template = get_node_by_pattern(nodes, 'helpBtn')[0]

    selects = get_node_by_pattern(nodes, 'select_[0-9]')
    items = get_node_by_pattern(nodes, 'item_[0-9]')
    pull_down_panels = get_node_by_pattern(nodes, 'node_pulldown')
    pull_down_btns = get_node_by_pattern(nodes, 'btn_pulldown')
    item_lists = get_node_by_pattern(nodes, 'item_list')
    help_btns = get_node_by_pattern(nodes, "btn_help")

    # for node in selects:
    #     node_name = node.getAttribute('Name')
    #     print node_name
    #     copy_child_attrs_by_arr(radio_template, node, ['DisabledFileData', 'PressedFileData', 'NormalFileData', 'Size'])
    #
    # for item in items:
    #     node_name = item.getAttribute('Name')
    #     print node_name
    #     copy_child_attrs_by_arr(radio_template, item, ['DisabledFileData', 'PressedFileData', 'NormalFileData', 'Size'])

    for pull_down in pull_down_panels:
        node_name = pull_down.getAttribute('Name')
        print node_name
        copy_child_attrs_by_arr(pull_down_panel_template, pull_down, ['Size', 'FileData'])

    # for btn in pull_down_btns:
    #     node_name = btn.getAttribute('Name')
    #     print node_name
    #     copy_child_attrs_by_arr(pull_down_btn_template, btn, ['DisabledFileData', 'PressedFileData', 'NormalFileData', 'Size'])
    #
    # for item_list in item_lists:
    #     node_name = item_list.getAttribute('Name')
    #     print node_name
    #     copy_child_attrs_by_arr(pull_down_panel_template, item_list, ['FileData'])
    #
    # for help_btn in help_btns:
    #     node_name = help_btn.getAttribute('Name')
    #     print node_name
    #     copy_child_attrs_by_arr(help_btn_template, help_btn, ['DisabledFileData', 'PressedFileData', 'NormalFileData', 'Size'])

    # players_node = get_node_by_pattern(nodes, r'player{1,2}[0-9]')
    # replace_node_name = ['maimaIcon']
    #
    # player1 = players_node[0]
    # for node_name in replace_node_name:
    #     for p in players_node[1:]:
    #         name = p.getAttribute('Name')
    #         print name + ' start'
    #         copy_child_attrs_by_arr(player1, p, ['Size'])
    #         print node_name + '========'
    #         node1 = get_node_by_name(p, node_name)
    #         node2 = get_node_by_name(player1, node_name)
    #         copy_child_attrs(node2, node1)
    #
    #         print name + ' end'
    #
    with open(xml_file, 'w') as fh:
        dom.writexml(fh)







