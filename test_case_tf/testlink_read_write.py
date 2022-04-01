# -*- encoding: utf-8 -*-
'''
@文件        :testlink_read_write.py
@说明        :读取或写入xml格式的testlink文件
@时间        :2022/03/16 10:01:36
@作者        :misldy.top
'''
import logging
import xml.etree.ElementTree as ET

class TestLinkProcessing:
    def xml_root_to_list(self, root, node_name=None):
        case_list = []
        for child in root:
            if child.tag == "testsuite":
                # 检查并转换node_name
                if node_name:
                    if child.attrib.get('name'):
                        child_name = node_name + '|' + child.attrib.get('name')
                    else:
                        child_name = node_name + '|未分类'
                else:
                    child_name = child.attrib.get('name')
                case_list.extend(self.xml_root_to_list(child, child_name))
            elif child.tag == 'testcase':
                # 获取用例名称
                name = child.attrib.get('name')
                # 获取用例分组
                group = node_name
                for case in child:
                    # 获取用例摘要
                    if case.tag == 'summary':
                        summary = case.text
                    # 获取用例前置条件
                    if case.tag == 'preconditions':
                        preconditions = case.text
                    # 获取用例等级
                    if case.tag == 'importance':
                        i = case.text
                        importance = (i=='3' and 'P0' or (i=='2' and 'P1' or (i=='1' and 'P2' or 'P3')))
                    # 获取用例操作步骤
                    if case.tag == 'steps':
                        actions, expectedresults = [], []
                        for step in case:
                            actions.append('【' + str(step[0].text) + '】' + str(step[1].text) + "；")
                            expectedresults.append('【' + str(step[0].text) + '】' + str(step[2].text))
                case_list.append({'name': name, 'group': group, 'summary': summary,
                                  'preconditions': preconditions, 'importance': importance,
                                  'actions': actions, 'expectedresults': expectedresults})
            else:
                continue
        return case_list
    
    def read_xml_cases(self, file_path):
        try:
            # 获取用例根目录内容
            root = ET.ElementTree(file=file_path).getroot()
            # 读取xml文件内容并转换为dict
            root_name = root.attrib.get('name')
            return self.xml_root_to_list(root, root_name)
        except ET.ParseError as ParseError:
            logging.error(f"xml文件存在多个根节点，无法解析！错误代码：{ParseError}")
            raise ParseError
        except Exception as e:
            logging.error(f"xml文件读取异常！错误代码：{e}")
            raise e
    
    def write_xml_cases(self):
        pass
    
if __name__ == '__main__':
    pass