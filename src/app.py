import gradio as gr

from rag import search_with_rbac, generate_answer


def ask_question(role, query):

    if not query.strip():
        return "Please enter a question.", ""

    retrieved, allowed, dropped = search_with_rbac(
        query,
        role
    )

    answer = generate_answer(
        query,
        allowed,
        role
    )

    if allowed:
        status = "Access granted to authorized information."
    else:
        status = "No authorized information was available for this question."

    return answer, status


with gr.Blocks(title="Secure Enterprise RAG") as app:

    gr.Markdown(
        """
        # 🔐 Secure Enterprise RAG

        Ask questions using your authorized role.
        The system retrieves relevant documents and applies
        RBAC before sending context to the LLM.
        """
    )

    with gr.Row():

        role = gr.Dropdown(
            choices=[
                "admin",
                "manager",
                "employee",
                "auditor"
            ],
            value="employee",
            label="Select Your Role"
        )

    query = gr.Textbox(
        label="Enter Your Question",
        placeholder="Ask a question about company policies...",
        lines=4
    )

    ask_button = gr.Button(
        "Ask Question",
        variant="primary"
    )

    status = gr.Textbox(
        label="Security Status",
        interactive=False
    )

    answer = gr.Textbox(
        label="Answer",
        lines=10,
        interactive=False
    )

    ask_button.click(
        fn=ask_question,
        inputs=[role, query],
        outputs=[answer, status]
    )


if __name__ == "__main__":
    app.launch()