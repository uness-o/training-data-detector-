import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME     = os.getenv("MODEL_NAME", "gpt-4")
client         = OpenAI(api_key=OPENAI_API_KEY)

def identify_in_training(text: str) -> str:
    if not OPENAI_API_KEY:
        return "Error: OPENAI_API_KEY not found in environment"
    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system",
                 "content": "Please act as an identification assistant ... Respond only with \"Yes\" or \"No\"."},
                {"role": "user",
                 "content": f"Please tell me whether … in the training dataset: {text}"}
            ],
            temperature=0.0,
            max_tokens=10
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# **Define demo at module scope** so the reloader can find it:
demo = gr.Blocks()

with demo:
    gr.Markdown("# Training Set Identification Assistant")
    gr.Markdown(f"Enter a piece of text below, then click **Identify** …\n\n"
                f"(Using model: **{MODEL_NAME}**, loaded from .env)")

    text_input = gr.Textbox(lines=4, label="Input Text")
    identify_button = gr.Button("Identify")
    output = gr.Textbox(label="Response (Yes/No)")

    identify_button.click(
        fn=identify_in_training,
        inputs=[text_input],
        outputs=output
    )

if __name__ == "__main__":
    demo.launch()
