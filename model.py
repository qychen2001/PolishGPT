from langchain.llms import OpenAI
from langchain.prompts import Prompt
import openai

import gradio as gr


FEACTURE_DICT = {
    "更精确的措辞": "More precise: Use more precise terms, such as 'generate' instead of 'produce' or 'analyze' instead of 'look at'.",
    "更简练的表达": "More concise: Eliminate unnecessary words and phrases to make the sentences clearer and more direct.",
    "更客观的语言": "More objective: Present information in a neutral manner by removing subjective language.",
    "更具体的描述": "More specific: Provide more specific details to support arguments or ideas.",
    "更连贯的表达": "More coherent: Ensure well-organized and logically flowing sentences.",
    "更一致的风格": "More consistent: Maintain consistency in language and style with the rest of the paper.",
    "更符合学术风格": "More academic: Use commonly used academic terms and phrases, such as 'furthermore' and 'thus'.",
    "更正式的语法": "More formal grammar: Utilize correct grammar and syntax, avoiding sentence fragments or off-topic sentences.",
    "更具细节的描述": "More nuanced: Convey more complex or subtle meanings by using specific words or phrases, making the sentences more nuanced."
}

LEVEL_DICT = {
    "仅对文本进行微调": "Subtle edits only",
    "进行一些小的编辑": "Minor edits",
    "改写以提高表达清晰度": "Rephrase for clarity",
    "简化句子结构": "Simplify sentence structure",
    "检查语法和拼写": "Check grammar and spelling",
    "提高文本流畅度和连贯性": "Enhance flow and coherence",
    "改善用词": "Improve word choice",
    "为文本调整风格": "Revise for style",
    "进行重大编辑": "Significant edits",
    "重新构建内容": "Restructure content"
}

TYPE_DICT = {
    "会议": "conference",
    "期刊": "journal"
}

DOMAIN_DICT = {
    "人工智能": "artificial intelligence",
    "计算机视觉": "computer vision",
    "自然语言处理": "natural language processing",
    "机器学习": "machine learning"
}


def format_proxy(proxy):
    if proxy is None:
        return None
    else:
        return "http://" + proxy.replace("http://", "").replace("https://", "")


def ask_gpt(prompt, api_key, proxy, model_name="gpt-3.5-turbo", temperature=0):
    openai.api_key = api_key
    openai.proxy = proxy
    try:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        ).choices[0].message['content']
        return response
    except Exception as e:
        openai.api_key = None
        openai.proxy = None
        return f"请求时发生错误，请重试！ {str(e)}"


def check_available(api_key, proxy=None, model_name="gpt-3.5-turbo"):
    openai.api_key = api_key
    openai.proxy = proxy
    try:
        openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": "Hello!"}],
            temperature=0,
        )
    except Exception as e:
        openai.api_key = None
        openai.proxy = None
        return f"检查可用性时发生了错误: {str(e)}"
    return "模型可用！"


def polish_prompt(polish_level, features_p, length_req, length, input_text, paper_type, paper_domain):
    if length_req == "扩写":
        length_prompt = f"Expand the original content to {length} words."
    elif length_req == "缩写":
        length_prompt = f"Condense the original content to {length} words."
    else:
        length_prompt = "Keep the original length."

    features_prompt = ""
    if len(features_p) != 0:
        # 把feature_p中的所有内容添加到一个字符串
        features_prompt = "\n".join(FEACTURE_DICT[key] for key in features_p)

    prompt = f"""Assume you are an expert in the {DOMAIN_DICT[paper_domain]}, and you excel at writing {TYPE_DICT[paper_type]} papers in this field. 
You are exceptionally skilled at polishing a piece of text to meet publication standards.
Your task is to refine the input text to meet publication standards based on the requirements.
The input text is enclosed in triple single quotation marks ('''), for example: '''This is the input text.'''
For the input text, you need to {LEVEL_DICT[polish_level]}. And you need to {length_prompt}.
The more detailed requirements are as follows:
{features_prompt}

The input text is:
'''
{input_text}
''' 
The polished text should be enclosed in <<<>>>. For example: <<<This is the polished text.>>>    
"""
    return prompt


def polish(polish_level, features_p, length_req, length, input_text, paper_type, paper_domain, api_key, proxy=None,
           model_name="gpt-3.5-turbo", temperature=0):
    prompt = polish_prompt(polish_level, features_p, length_req, length, input_text, paper_type, paper_domain)
    return ask_gpt(prompt, api_key, proxy, model_name, temperature).strip("<<<").strip(">>>")


