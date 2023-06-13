import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from instruct_pipeline import InstructionTextGenerationPipeline
import json

model = "databricks/dolly-v2-3b"
tokenizer = AutoTokenizer.from_pretrained(model, padding_side="left")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForCausalLM.from_pretrained(
    model,
    pad_token_id=tokenizer.eos_token_id,
    device_map="auto",
    torch_dtype=torch.bfloat16,
)
model = model.to("cuda" if torch.cuda.is_available() else "cpu")
model.eval()

generate_text = InstructionTextGenerationPipeline(model=model, tokenizer=tokenizer)

canvas_html = (
    "<chat-feeback style='display:flex;justify-content:center;'></chat-feeback>"
)
load_js = """
async () => {
  const script = document.createElement('script');
  script.type = "module"
  script.src = "file=index.js"
  document.head.appendChild(script);
}
"""


def accept_response(rating_dummy, msg, chatbot, responseA, responseB, selection_state):
    ratings = json.loads(rating_dummy)

    state = [
        ratings["label"],
        ratings["value"],
        responseA if ratings["label"] == "A" else responseB,
    ]

    selection_state = selection_state + [state]
    chatbot = [[msg, state[2]]]

    return chatbot, selection_state, selection_state


def generate(msg, history):
    user_message = msg
    responses = []
    for i in range(2):
        res = generate_text(
            user_message,
            max_new_tokens=50,
            top_p=0.9 if i == 0 else 0.5,
            top_k=500,
            do_sample=True,
        )
        responses.append(res[0]["generated_text"])
    return responses


with gr.Blocks() as blocks:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    responseA = gr.Textbox(label="Response A")
    responseB = gr.Textbox(label="Response B")
    rating_dummy = gr.Textbox(elem_id="rating-dummy", interactive=False, visible=False)
    ratings_buttons = gr.HTML(canvas_html, visible=False)

    selection_state = gr.State(value=[])
    selections_df = gr.Dataframe(
        type="array",
        headers=["Option", "Value", "Text"],
        label="Selections",
    )

    def user(user_message, history):
        return gr.update(value="", interactive=False), history + [[user_message, ""]]

    def bot(history):
        user_message = history[-1][0]
        res = generate_text(
            user_message, max_new_tokens=50, top_p=0.9, top_k=500, do_sample=True
        )
        print(res)
        chat_history = history[-1][1] + res[0]["generated_text"]
        new_history = history[:-1] + [[user_message, chat_history]]
        yield new_history

    response = (
        msg.submit(
            lambda: (gr.update(interactive=False), gr.update(visible=False)),
            inputs=None,
            outputs=[msg, ratings_buttons],
        )
        .then(generate, inputs=[msg, chatbot], outputs=[responseA, responseB])
        .then(lambda: gr.update(visible=True), inputs=None, outputs=[ratings_buttons])
    )
    rating_dummy.change(
        accept_response,
        inputs=[rating_dummy, msg, chatbot, responseA, responseB, selection_state],
        outputs=[chatbot, selection_state, selections_df],
    ).then(
        lambda: (
            gr.update(value="", interactive=True),
            gr.update(visible=False),
            gr.update(value=""),
            gr.update(value=""),
        ),
        inputs=None,
        outputs=[msg, ratings_buttons, responseA, responseB],
    )
    response.then(
        lambda: gr.update(interactive=True), inputs=None, outputs=[msg], queue=False
    )
    blocks.load(None, None, None, _js=load_js)

blocks.queue()
blocks.launch()
