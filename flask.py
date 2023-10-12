import gradio as gr
from model import check_available, polish, ask_gpt


with gr.Blocks() as interface:
    gr.Markdown(
        value="""
        # PolishGPT: 用GPT改善你的论文写作！
        由于每次都要用ChatGPT润色都要写复杂的Prompt，所以我设计了一个WebUI，可以快速润色论文。
        **这个项目由[陈启源](https://qiyuan-chen.github.io/) @ 华中师范大学 and 浙江大学 开发。**
        """)
    with gr.Row():
        with gr.Tab("基础设置"):
            with gr.Row():
                with gr.Column():
                    api_key = gr.Textbox(label="OpenAI API Key")
                    temperature = gr.Slider(minimum=0.0, maximum=1.0, value=0, step=0.1, label="Temperature",
                                            info="控制生成文本的随机性。数值越小，模型的确定性越高")
                with gr.Column():
                    model_name = gr.Dropdown(choices=["gpt-3.5-turbo", "gpt-4"], label="使用的模型",value="gpt-3.5-turbo")
                    check = gr.Button(value="检查可用性")
                with gr.Column():
                    proxy = gr.Textbox(label="代理地址，在国内使用需要设置", value="http://192.168.0.124:7890")
                    check_status = gr.Textbox(label="检查结果")
                check.click(check_available, inputs=[api_key, proxy, model_name], outputs=[check_status])
                with gr.Column():
                    paper_type = gr.Dropdown(choices=["会议", "期刊"], label="论文类型",value="会议")
                    paper_domain = gr.Dropdown(choices=['人工智能', '自然语言处理', '计算机视觉', '机器学习'],
                                               label="论文领域",value="人工智能")

        # with gr.Tab("语言风格设置"):

    with gr.Row():
        with gr.Tab("润色"):
            # 润色程度
            polish_level = gr.Dropdown(
                choices=["仅对文本进行微调", "进行一些小的编辑", "改写以提高表达清晰度", "简化句子结构",
                         "检查语法和拼写", "提高文本流畅度和连贯性", "改善用词", "为文本调整风格", "进行重大编辑",
                         "重新构建内容"], label="润色程度/功能",value="改写以提高表达清晰度")
            features_p = gr.Checkboxgroup(
                choices=["更精确的措辞", "更简练的表达", "更客观的语言", "更具体的描述", "更连贯的表达", "更一致的风格",
                         "更符合学术风格", "更正式的语法", "更具细节的描述"], label="具体要求",
                info="此选项不建议一次选太多！",value=['更精确的措辞'])
            length_req = gr.Dropdown(choices=["保持原长度", "扩写", "缩写"], label="文本长度要求",value="保持原长度")
            length = gr.Slider(minimum=20, maximum=2000, step=10, label="生成文本长度",
                               info="控制润色后的文本长度，当文本长度要求设置为保持原长度时，这一选项不起作用")
            input_text_1 = gr.Textbox(lines=6, label="润色前的文本",value="请输入需要润色的文本！")
            output_text_1 = gr.Textbox(lines=6, label="润色后的文本", show_copy_button=True)
            submit_1 = gr.Button(value="开始润色")

            submit_1.click(fn=polish,
                           inputs=[polish_level, features_p, length_req, length, input_text_1, paper_type, paper_domain,
                                   api_key, proxy, model_name, temperature], outputs=[output_text_1])

        with gr.Tab("翻译"):
            features_t = gr.Checkboxgroup(
                choices=["更精确的措辞", "更简练的表达", "更客观的语言", "更具体的描述", "更连贯的表达", "更一致的风格",
                         "更符合学术风格", "更正式的语法", "更具细节的描述"])
            with gr.Row():
                with gr.Column():
                    source_language = gr.Dropdown(choices=["中文", "英文"], label="源语言", value="英文")
                with gr.Column():
                    target_language = gr.Dropdown(choices=["中文", "英文"], label="目标语言", value="中文")
            input_text_2 = gr.Textbox(lines=6, label="翻译前的文本")
            output_text_2 = gr.Textbox(lines=6, label="翻译后的文本", show_copy_button=True)
            submit_2 = gr.Button(label="开始翻译", )

        with gr.Tab("要点生成段落"):
            input_text_3 = gr.Textbox(lines=6, label="输入要点")
            output_text_3 = gr.Textbox(lines=6, label="输出文本", show_copy_button=True)
            submit_3 = gr.Button(label="开始生成")


interface.launch(server_name='192.168.0.242',server_port=7860)