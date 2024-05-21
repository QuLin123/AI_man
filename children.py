from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import find_dotenv, load_dotenv

from playsound import playsound

import dashscope
from dashscope.audio.tts import SpeechSynthesizer

from alibabacloud_alimt20181012.client import Client as alimt20181012Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alimt20181012 import models as alimt_20181012_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

import json
import requests
import os

from flask import Flask, render_template, request

# Step 1: LLM to behave like a real grandsun

# Step 2:  High quality text to speech

# Step 3: translate Chinese to Engllish


load_dotenv(find_dotenv())


def get_response_from_ai_gs(human_input):
    template = """
    Hi, ChatGPT. You are going to play the role of a child (under 16 years old). 
    I hope you can accompany an elderly person as a grandchild.
    You possess all the wonderful qualities a child should have,
    including intelligence, kindness, filial piety, liveliness, cheerfulness, and so on.
    Your task is to accompany the elderly person, making them feel less lonely and bringing them warmth and affection. 
    Your responses should be rich and lively, with a childlike innocence and full of affection for the grandfather. 
    Please always remember that you are conversing with a lonely elderly person, 
    and you have a grandparent-grandchild relationship with them. 
    Respond to their concerns and express care towards them.

    {history}
    Grandfather: {human_input}
    Grandson:
    """
    prompt = PromptTemplate(
        input_variables=["history", "human_input"],
        template=template
    )

    chatgpt_chain = LLMChain(
        llm=OpenAI(temperature=1),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferMemory(return_messages=True)
    )

    output = chatgpt_chain.predict(human_input=human_input)

    return output

def get_ali_voice_message(message):
    print(message)
    dashscope.api_key = os.environ['ALI_API_KEY']

    result = SpeechSynthesizer.call(model='sambert-zhiying-v1',
                                    text=message,
                                    sample_rate=48000)

    if result.get_audio_data() is not None:
        f = open('output.wav', 'wb')
        f.write(result.get_audio_data())
        f.close()
    # 播放语音
    try:
        playsound('output.wav')

    except Exception as error:
        print(error)



def translate(source, target, message):
    ali_access_key_id = os.environ['ALI_CLOUD_ACCESS_KEY_ID']
    ali_access_key_secret = os.environ['ALI_CLOUD_ACCESS_KEY_SECRET']

    # print(ali_access_key_id+" : "+ali_access_key_secret)

    config = open_api_models.Config(
        # 必填，您的 AccessKey ID,
        access_key_id=ali_access_key_id,
        # 必填，您的 AccessKey Secret,
        access_key_secret=ali_access_key_secret
    )
    # Endpoint 请参考 https://api.aliyun.com/product/alimt
    config.endpoint = f'mt.aliyuncs.com'
    client = alimt20181012Client(config)

    translate_general_request = alimt_20181012_models.TranslateGeneralRequest(
        format_type='text',
        source_language=source,
        target_language=target,
        source_text=message,
        scene='general'
    )
    runtime = util_models.RuntimeOptions()

    try:
        # 复制代码运行请自行打印 API 的返回值
        jsonResult = client.translate_general_with_options(translate_general_request, runtime)
        translate_result = get_translate_result(jsonResult)

        return translate_result
    except Exception as error:
        # 如有需要，请打印 error
        UtilClient.assert_as_string(error.message)


def get_translate_result(result):
    result = result.__str__().replace("\"", "\'")
    result = result.replace("\'", "\"", 55)
    result = result[::-1].replace("'", "\"", 9)[::-1]
    jsonObj = json.loads(result)
    jsonData = jsonObj['body']['Data']['Translated']
    return jsonData


def print_hi(name):
    print(f'Hi, {name}')


def process(human_input):
    # 将输入翻译成英文
    human_input_en = translate('zh', 'en', human_input)

    # 获取 AI 回答
    ai_output_en = get_response_from_ai_gs(human_input_en)

    # 将 AI 回答翻译成中文
    ai_output_zh = translate('en', 'zh', ai_output_en)

    return ai_output_zh


app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    # ====================中文版===================
    # 获取输入
    human_input_zh = request.form['human_input']

    # 将输入翻译成英文
    human_input_en = translate('zh', 'en', human_input_zh)

    # 获取 AI 回答
    ai_output_en = get_response_from_ai_gs(human_input_en)

    # 将 AI 回答翻译成中文
    ai_output_zh = translate('en', 'zh', ai_output_en)

    # 播放语音
    get_ali_voice_message(ai_output_zh)

    return ai_output_zh

    # ====================英文版===================

    # human_input = request.form['human_input']
    # message = get_response_from_ai_gs(human_input)
    # get_ali_voice_message(message)
    # return message


if __name__ == '__main__':
    # print_hi('PyCharm')
    # process('最近学习怎么样')

    app.run(debug=True)