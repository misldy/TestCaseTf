# -*- encoding: utf-8 -*-
'''
@文件        :case_tf_demo.py
@说明        :testlink测试用例转换为TMP格式
@时间        :2022/03/16 10:01:36
@作者        :misldy.top
'''
import pandas as pd, os, logging, xml.etree.ElementTree as ET, re

class TestLinkToTmp:
    def __init__(self, xml_path, excel_path):
        self.xml_path = xml_path
        self.excel_path = excel_path
    
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
                print(dir())
                if 'actions' not in dir():
                    actions = ""
                if 'expectedresults' not in dir():
                    expectedresults = ""
                case_list.append({'name': name, 'group': group, 'summary': summary,
                                  'preconditions': preconditions, 'importance': importance,
                                  'actions': actions, 'expectedresults': expectedresults})
            else:
                continue
        return case_list
    
    @property
    def read_xml_cases(self):
        try:
            # 获取用例根目录内容
            root = ET.ElementTree(file=self.xml_path).getroot()
            # 读取xml文件内容并转换为dict
            root_name = root.attrib.get('name')
            return self.xml_root_to_list(root, root_name)
        except ET.ParseError as ParseError:
            logging.error(f"xml文件存在多个根节点，无法解析！错误代码：{ParseError}")
            raise ParseError
        except Exception as e:
            logging.error(f"xml文件读取异常！错误代码：{e}")
            raise e
    
    def to_tmp_excel(self):
        # 整理数据未TMP平台需要的格式
        data = []
        list_group = []
        case_list = self.read_xml_cases
        for case in case_list:
            # 获取数据group信息，并处理成TMP平台格式
            group = case.get('group')
            if not group:
                group = "未分类"
            group_split = group.split('|')
            case_id = len(group_split) + 1
            for (g, i) in zip(group_split, range(1, case_id)):
                if g not in list_group:
                    case_group = {"": i, "目录名称": g, "用例标题": "", "优先级": "",
                                 "预置条件": "", "操作步骤": "", "预期结果": ""}
                    data.append(case_group)
                    list_group.append(g)

            # 获取数据case信息，并处理成TMP平台格式
            name = case.get('name')
            importance = case.get('importance')
            preconditions = case.get('preconditions')
            importance = re.sub(r"<p>|</p>", os.linesep, str(importance))
            importance = re.sub(r"&nbsp;", "", str(importance))
            preconditions = re.sub(r"<p>|</p>", os.linesep, str(preconditions))
            preconditions = re.sub(r"&nbsp;", "", str(preconditions))            
            actions = case.get('actions')
            expectedresults = case.get('expectedresults')
            action_str, expectedresult_str = '', ''
            for action in actions:
                action = re.sub(r"<p>|</p>", os.linesep, str(action))
                action = re.sub(r"&nbsp;", "", str(action))
                action_str += action + os.linesep
            for expectedresult in expectedresults:
                expectedresult = re.sub(r"<p>|</p>", os.linesep, str(expectedresult))
                expectedresult = re.sub(r"&nbsp;", "", str(expectedresult))
                expectedresult_str += expectedresult + os.linesep
            case_dict = {"": case_id, "目录名称": "", "用例标题": name, "优先级": importance,
                         "预置条件": preconditions, "操作步骤": action_str, "预期结果": expectedresult_str}
            data.append(case_dict)
        
        # 数据转换为excel格式
        df = pd.DataFrame(data)
        with pd.ExcelWriter(self.excel_path) as f:
            sheet_name = os.path.basename(self.excel_path.split('.')[0])
            if not sheet_name:
                sheet_name = 'Sheet1'
            df.to_excel(f, index=False, sheet_name=sheet_name)
        

if __name__=="__main__":
    pass
