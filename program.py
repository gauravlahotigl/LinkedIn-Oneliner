import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import requests

json_response = []
summary = []
message = []

# Proxycurl api: 'xTUADCs_xYgM3_aLbS94xw'
# chatGPT api: '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'

def getJsonData(pandas_dataframe,url_column_name:str,proxycurl_key:str):
    urls = pandas_dataframe[url_column_name][:25]
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    header_dic = {'Authorization': 'Bearer ' + proxycurl_key}
    for i in urls:
        try:
            params = {
                'url': str(i),
                'fallback_to_cache': 'on-error',
                'use_cache': 'if-present',
                'skills': 'include',
            }
            response = requests.get(api_endpoint,
                                    params=params,
                                    headers=header_dic)
            json_response.append(response.json())
        except:
            print('There was a problem fetching the LinkedIn data')
    print('Fetching of LinkedIn Data Successfull')
        

def getSummaryOfProfile():
    content = ''
    for i in json_response:
        try:
            if i['summary'] != None:
                content += i['summary']
                content += ' ' + str(i['accomplishment_honors_awards'])
                content += ' ' + str(i['headline'])
                content += ' ' + str(i['education'])
                summary.append([content])
                
            else:
                content += str(i['accomplishment_honors_awards'])
                content += ' ' + str(i['headline'])
                content += ' ' + str(i['education'])
                summary.append([content])
        except:
            summary.append([])
            print('There was a problem fetching profile')
        content = ''
    print('Summary of profiles was generated successfully')
    

def chatgptResponse(api_key:str, pandas_dataframe):
    bot = ChatOpenAI(temperature=1, openai_api_key=api_key)
    for i in summary:
        message.append(bot(
            [
                SystemMessage(content='''
                    You are a very intelligent bot which gives an attention seeking one line personalised appreciation 
                    highlighting person's acheivements and skills but remember that the word count should not exceed 
                    25-30 words. But the message should'nt be a generic message and the pronoun that you use should be
                    with respect to the person.
                    For example:
                    
                    input: Alan is an experieced FullStack developer with skills of HTML5, CSS3, ReactJS and NodeJS. He has
                        been working as a backend developer in a company which provides software solutions to the businesses.
                    output: your FullStack prowess with HTML5, CSS3, ReactJS, and NodeJS shines brightly, intertwining innovative 
                            backend solutions that propel businesses forward. Your dedication and expertise make a remarkable difference 
                            in delivering tailored software solutions that cater to your clients' unique needs. 
                            
                    input: []
                    output: Sorry the profile was not found
                '''),
                HumanMessage(content=str(i))
            ]
        ).content)
    pandas_dataframe['CHATGPTResponse'] = message
    pandas_dataframe.to_csv('final_data.csv')   
    print('ChatGPT Responded Successfull')
    

# getJsonData(df2,'Linkedin URL','xTUADCs_xYgM3_aLbS94xw')
# getSummaryOfProfile(json_response)
# chatgptResponse('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', df2)