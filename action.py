from openai import OpenAI
import pandas as pd
import glob
import numpy as np
import csv
import json
# 定义系统消息
#system_message = "I'll give you a few words, you need to change things like objectxxx (like object01, object12) into chair, just chair. There may be multiple sentences, you need to do this action on all sentences and keep the structure of the sentences. And you need to keep the #xxx#xxx at the end of the sentence, like #109#146"
#system_message="I will give you a few words, some name of the object is connected together, and you need to change them back, for example, you need to change the things like chairsmall into a small chair, change standfordbunny to Standford bunny. But only change when there's need for change, if it's just a chair, keep it don't change it to small chair, and don't add extra #. There may be multiple sentences, you need to do this action on all sentences and keep the structure of the sentences. And you need to keep the #xxx#xxx in the end of the sentence, like #109#146.Delete the extra \" in the input, and change to a new line after the #xxx#xxx, not before it"
system_message="I'll give you a few sentences, and you need to choose the one best word to describe the whole sentences in the set [Carry,Sit,Swing,Exercise,Rotate,Move,Hold,Drink,Eat,Play,Adjust,Lift,Kick,Pass,Manipulate,Skateborad].You answer should be only one word "
total_tokens = 0
    


csv_files = glob.glob('./omomo_text_anno_json_data/*.json')

# 初始化一个空的DataFrame用于之后的数据合并
csv_file_name = 'relations.csv'
# 步骤 3: 遍历所有找到的CSV文件
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 写入列名
    writer.writerow(['Name', 'Answer.action'])
    for file in csv_files:
        # 读取每个CSV文件
        with open(file, 'r') as f:
            data = json.load(f)
        # 筛选出AssignmentStatus为'Approved'的行
        #filtered_df = df
        key=next(iter(data))
        text=data[key]
        user_content=text
        user_message = {"role": "user", "content": user_content}
    
            # 构建当前请求的消息列表，只包含系统消息和当前用户消息
        messages = [{"role": "system", "content": system_message}, user_message]
    
            # 重新初始化 OpenAI 客户端
        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages
        )
    
        response_message = completion.choices[0].message
        response = response_message.content
        usage=completion.usage
        total_tokens += usage.total_tokens
        print(usage)
        print(response)
        print(f"Tokens used for this completion: {usage.total_tokens}")
        print(f"Total tokens used so far: {total_tokens}")
        writer.writerow([key,response])
        """
        df_numpy=np.array(filtered_df)
        for i in range(df_numpy.shape[0]):
            user_content=df_numpy[i][4]
            user_message = {"role": "user", "content": user_content}
    
            # 构建当前请求的消息列表，只包含系统消息和当前用户消息
            messages = [{"role": "system", "content": system_message}, user_message]
    
            # 重新初始化 OpenAI 客户端
            client = OpenAI()
            completion = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=messages
            )
    
            response_message = completion.choices[0].message
            response = response_message.content
            df_numpy[i][4]=response
            usage = completion.usage
            total_tokens += usage.total_tokens
            print(usage)
            print(response)
            print(f"Tokens used for this completion: {usage.total_tokens}")
            print(f"Total tokens used so far: {total_tokens}")

        writer.writerows(df_numpy)
        """

print(f"Total tokens used: {total_tokens}")
