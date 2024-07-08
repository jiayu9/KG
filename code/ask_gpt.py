import openai 
import pandas as pd
import os

GPT_API_KEY=os.getenv('GPT_API_KEY')
openai.api_key=GPT_API_KEY

client=openai.OpenAI()
KG_sample_file=client.files.create(
  file=open("../data/sample.csv", "rb"),
  purpose="fine-tune"
)

chatlog=[]

def logical_query_to_question(query):
    user_message = open("user_message1","r").read()+str(query)
    
    response=openai.ChatCompletion.create(
        model='gpt-4o',
        messages={'role': 'user', 'content': user_message}
    )
    
    question=response['choices'][0]['message']['content']
    return question

def question_to_entity(question):
    user_message = open("user_message2","r").read()+str(question)
    
    response=openai.ChatCompletion.create(
        model='gpt-4o',
        messages={'role': 'user', 'content': 
                    [
                        {
                            'type':"text",
                            "text":user_message
                        },
                        {
                            "type":"file",
                            "text": KG_sample_file
                        }
                    ]
                }
    )
    
    pred_entity=response['choices'][0]['message']['content']
    return pred_entity

if __name__ == "__main__":
    df = pd.read_csv('../data/KG_LLM.csv')
    df['question']=logical_query_to_question(df['query'])
    df['pred_entity'] = question_to_entity(df['question'])
    df['match'] = df.apply(lambda row: 1 if row['GT'].lower() == row['pred_entity'].lower() else 0, axis=1)
    df.to_csv('query.csv', index=False)
    print(f'correct predictions:{df['match'].sum()} out of {len(df)}')