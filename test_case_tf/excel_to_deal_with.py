# -*- encoding: utf-8 -*-
'''
@文件        :excel_to_deal_with.py
@说明        :
@时间        :2022/03/16 10:14:02
@作者        :misldy.top
'''

import pandas as pd, os
from testlink_read_write import TestLinkProcessing

class ExcelProcessing:
    def __init__(self, case_list, excel_path):
        self.case_list = case_list
        self.excel_path = excel_path
    
    def to_tmp_excel(self):
        # 整理数据未TMP平台需要的格式
        data = []
        list_group = []
        for case in self.case_list:
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
            actions = case.get('actions')
            expectedresults = case.get('expectedresults')
            action_str, expectedresult_str = '', ''
            for action in actions:
                action_str += action + os.linesep
            for expectedresult in expectedresults:
                expectedresult_str += expectedresult + os.linesep
            case_dict = {"": case_id, "目录名称": "", "用例标题": name, "优先级": importance,
                         "预置条件": preconditions, "操作步骤": action_str, "预期结果": expectedresult_str}
            data.append(case_dict)
        
        # 数据转换为excel格式
        df = pd.DataFrame(data)
        with pd.ExcelWriter(self.excel_path) as f:
            df.to_excel(f, index=False)
        

if __name__=="__main__":
    pass