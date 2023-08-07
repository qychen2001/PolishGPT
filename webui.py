import gradio as gr

with gr.Blocks() as interface:
    with gr.Row():
        with gr.Tab("基础模型设置"):
            api_key = gr.Textbox(label="OpenAI API Key")
            proxy = gr.Textbox(label="代理地址，在国内使用需要设置")
            model_name = gr.Dropdown(choices=["gpt-3.5-turbo", "gpt-4"], label="使用的模型")
            temperature = gr.Slider(minimum=0.0, maximum=1.0, value=0, step=0.1, label="Temperature",
                                    info="控制生成文本的随机性。数值越小，模型的确定性越高")
        with gr.Tab("基础论文设置"):
            paper_type = gr.Dropdown(choices=["会议", "期刊"], label="论文类型")
            paper_domain = gr.Dropdown(choices=['人工智能', '自然语言处理', '计算机视觉', '机器学习'], label="论文领域")

        # with gr.Tab("语言风格设置"):

    with gr.Row():
        with gr.Tab("润色"):
            # 润色程度
            polish_level = gr.Dropdown(choices=[])
            input_text = gr.Textbox(lines=6, label="润色前的文本")
            output_text = gr.Textbox(lines=6, label="润色后的文本", show_copy_button=True)
            submit = gr.Button(label="开始润色")

        with gr.Tab("翻译"):
            with gr.Row():
                with gr.Column():
                    source_language = gr.Dropdown(choices=["中文", "英文"], label="源语言")
                with gr.Column():
                    target_language = gr.Dropdown(choices=["中文", "英文"], label="目标语言")
            input_text = gr.Textbox(lines=6, label="翻译前的文本")
            output_text = gr.Textbox(lines=6, label="翻译后的文本", show_copy_button=True)
            submit = gr.Button(label="开始翻译")

        with gr.Tab("要点生成段落"):
            input_text = gr.Textbox(lines=6, label="输入要点")
            output_text = gr.Textbox(lines=6, label="输出文本", show_copy_button=True)
            submit = gr.Button(label="开始生成")

interface.launch()
