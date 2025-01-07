# @Author : jerry-official
# @File : transformer.py
# @Project : question_transformer
import json
import os

with open('日志.log', 'w',encoding='UTF-8') as f:
    print('作者: jerry-official@github', file=f)
    def convert_questions_to_df(input_file, output_file):
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            lines = infile.readlines()
            num_questions = (len(lines)-2) // 7  # 每7行一个题目
            print(f'总行数为{(len(lines)+1)}，应该有{num_questions}个题目', file=f)
            if (len(lines)+1) >= 3:
                header = (
                    '{\n  "alias": "' + lines[0].strip().replace('"', " ' ") + '",\n  "description": "' + lines[1].strip().replace('"', " ' ") + '",\n  "star": ' + lines[2].strip().replace('"', " ' ") + ',\n  "problems": [\n'
                )

                outfile.write(header)
            else:
                print('error 行数小于3，不存在标头\nerror error error error error error error error error error error error', file=f)
            i = 3
            t = 0
            while i <= (len(lines)-5):
                content = lines[i].strip()  # 第一行是题干
                content = content.replace('"', " ' ")  # 将题干中的双引号替换为2个空格

                type_and_answer = lines[i + 1].strip()  # 第二行是题型和答案
                options = [lines[i + j].strip() for j in range(2, 6)]  # 第3-6行为选项
                options = str(options).replace('"', " ' ")

                question_type = type_and_answer[:3]  # 题型，取“单选题”或“多选题”
                answer_raw = type_and_answer[3:]  # 答案部分
                if question_type == "单选题" or question_type == "多选题":
                    if question_type == "单选题":
                        answer = int(answer_raw)  # 单选题答案是一个数字
                    if question_type == "多选题":
                        answer = [int(x) for x in answer_raw]  # 多选题答案是数字列表
                    question_dict = {
                        "content": content,
                        "options": options,
                        "answer": answer
                    }
                    formatted_str = (
                        ',\n    {'+'\n' +'      ' +'"content": "' + question_dict["content"] + '",\n' +
                        '      "options": ' + json.dumps(question_dict["options"], ensure_ascii=False) + ',\n' +
                        '      "answer": ' + json.dumps(question_dict["answer"], ensure_ascii=False) + '    ' +'\n    }'
                    )
                    if t == 0:
                        formatted_str = formatted_str[2:]
                    outfile.write(formatted_str)
                    i = i + 7
                    t = t + 1
                else:
                    print(f'error error error error error error error error error error error error\nerror 文件{input_file}第{i}行题型识别错误，请检查周围3题，并确定: \n1.没有多余的换行，2.确定"单选题"或"多选题"是题干下一行的前三个字',file=f)
                    i = i + 1

            end = (
                '\n  ]\n}\n'
            )
            outfile.write(end)
            print(f'{input_file}的题目转换完毕, 共计{t}个', file=f)

    # 获取目录下所有的txt文件
    y = 0
    n = 0
    for filename in os.listdir():
        if filename.endswith('.txt'):
            print(f'找到{filename}', file=f)
            if os.path.getsize(filename) != 0:
                input_file = os.path.join(filename)
                output_file = os.path.join(filename.replace('.txt', '.json'))  # 输出文件名为同名的.json文件
                print(f'开始转换{input_file}', file=f)
                convert_questions_to_df(input_file, output_file)
                y = y + 1
            else:
                print(f'error {filename}为空,不能进行转换\nerror error error error error error error error error error error error', file=f)
                n = n + 1
    if y + n == 0:
        print('error 当前目录下不存在txt文件\nerror error error error error error error error error error error error', file=f)
    else:
        print(f'同一目录下共有{y+n}个txt文件, 其中有{n}个空文件,{y}个文件转换完毕, 请注意是否有报错', file=f)
