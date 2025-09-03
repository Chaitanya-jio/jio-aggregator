import gradio as gr
from gradio_calendar import Calendar 
from datetime import datetime, timedelta
from utils.wildfire import search_papers_w, on_page_change_w
from utils.quantum import search_papers_q, on_page_change_q
from utils.ai import search_papers_ai, on_page_change_ai
from utils.blockchain import search_papers_b, on_page_change_b
from utils.all import search_papers_all, on_page_change_all

# replace your js string with this:
js = """
() => {
  try {
    const params = new URLSearchParams(window.location.search);
    const wanted = params.get("tab");           // e.g. ?tab=ai
    if (!wanted) return;

    // map short keys -> actual tab labels shown in the UI
    const map = {
      wildfire: "Wildfire prediction and forecasting using Deep learning",
      quantum_computing: "Quantum Computing",
      ai: "Artificial Intelligence",
      web3_blockchain: "Web3 and Blockchain",
    };

    const wantedLabel = map[wanted] || wanted;

    const tabs = Array.from(document.querySelectorAll("[role='tab']"));
    const slug = s => (s || "")
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "_")
      .replace(/^_|_$/g, "");

    // try exact match, case-insensitive, slug match, and prefix match
    let btn =
      tabs.find(t => t.innerText.trim() === wantedLabel) ||
      tabs.find(t => t.innerText.trim().toLowerCase() === wantedLabel.toLowerCase()) ||
      tabs.find(t => slug(t.innerText) === slug(wantedLabel)) ||
      tabs.find(t => slug(t.innerText).startsWith(slug(wanted)));

    if (btn) btn.click();
  } catch (e) {
    console.log("tab init error", e);
  }
}
"""


with gr.Blocks(theme=gr.themes.Soft(primary_hue="purple"), css="footer{display:none !important}") as demo:
    gr.Markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Roboto', sans-serif !important;
            }
            a {
                font-family: 'Roboto', sans-serif !important;
            }
        </style>
    
        <h1 style="text-align:center; color:#6f42c1; margin-bottom: 30px;">Latest Research Trends (ArXiv)</h1>
        """)
    
    with gr.Tab('Wildfire prediction and forecasting using Deep learning', id='wildfire'):
        with gr.Row():
            default_start_date = datetime.now() - timedelta(days=30)
            default_end_date = datetime.now()
            start_date = Calendar(value=default_start_date, label="📅 Start Date")
            end_date = Calendar(value=default_end_date, label="📅 End Date")

        search_btn = gr.Button("🔍 Search Papers", elem_id="search-btn", scale=2)
        status_output = gr.Textbox(label="Status", interactive=False)
        results_output = gr.HTML()
        page_buttons = gr.Radio(choices=[], label="📄 Pages", interactive=True, visible=False)

        search_btn.click(
            fn=search_papers_w,
            inputs=[start_date, end_date],
            outputs=[page_buttons, status_output, results_output, page_buttons]
        )

        page_buttons.change(
            fn=on_page_change_w,
            inputs=[page_buttons, start_date, end_date],
            outputs=results_output
        )

        demo.load(
        fn=search_papers_w,
        inputs=[start_date, end_date],
        outputs=[page_buttons, status_output, results_output, page_buttons],
        scroll_to_output=False
    )

    with gr.Tab('Quantum Computing', id='quantum_computing'):    
        with gr.Row():
            default_start_date = datetime.now() - timedelta(days=30)
            default_end_date = datetime.now()
            start_date = Calendar(value=default_start_date, label="📅 Start Date")
            end_date = Calendar(value=default_end_date, label="📅 End Date")
    
        search_btn = gr.Button("🔍 Search Papers", elem_id="search-btn", scale=2)
        status_output = gr.Textbox(label="Status", interactive=False)
        results_output = gr.HTML()
        page_buttons = gr.Radio(choices=[], label="📄 Pages", interactive=True, visible=False)
    
        search_btn.click(
            fn=search_papers_q,
            inputs=[start_date, end_date],
            outputs=[page_buttons, status_output, results_output, page_buttons]
        )
    
        page_buttons.change(
            fn=on_page_change_q,
            inputs=[page_buttons, start_date, end_date],
            outputs=results_output
        )

        demo.load(
        fn=search_papers_q,
        inputs=[start_date, end_date],
        outputs=[page_buttons, status_output, results_output, page_buttons],
        scroll_to_output=False
    )

    with gr.Tab('Artificial Intelligence', id='ai'):    
        with gr.Row():
            default_start_date = datetime.now() - timedelta(days=30)
            default_end_date = datetime.now()
            start_date = Calendar(value=default_start_date, label="📅 Start Date")
            end_date = Calendar(value=default_end_date, label="📅 End Date")
    
        search_btn = gr.Button("🔍 Search Papers", elem_id="search-btn", scale=2)
        status_output = gr.Textbox(label="Status", interactive=False)
        results_output = gr.HTML()
        page_buttons = gr.Radio(choices=[], label="📄 Pages", interactive=True, visible=False)
    
        search_btn.click(
            fn=search_papers_ai,
            inputs=[start_date, end_date],
            outputs=[page_buttons, status_output, results_output, page_buttons]
        )
    
        page_buttons.change(
            fn=on_page_change_ai,
            inputs=[page_buttons, start_date, end_date],
            outputs=results_output
        )

        demo.load(
        fn=search_papers_ai,
        inputs=[start_date, end_date],
        outputs=[page_buttons, status_output, results_output, page_buttons],
        scroll_to_output=False
    )

    with gr.Tab('Web3 and Blockchain', id='web3_blockchain'):    
        with gr.Row():
            default_start_date = datetime.now() - timedelta(days=30)
            default_end_date = datetime.now()
            start_date = Calendar(value=default_start_date, label="📅 Start Date")
            end_date = Calendar(value=default_end_date, label="📅 End Date")
    
        search_btn = gr.Button("🔍 Search Papers", elem_id="search-btn", scale=2)
        status_output = gr.Textbox(label="Status", interactive=False)
        results_output = gr.HTML()
        page_buttons = gr.Radio(choices=[], label="📄 Pages", interactive=True, visible=False)
    
        search_btn.click(
            fn=search_papers_b,
            inputs=[start_date, end_date],
            outputs=[page_buttons, status_output, results_output, page_buttons]
        )
    
        page_buttons.change(
            fn=on_page_change_b,
            inputs=[page_buttons, start_date, end_date],
            outputs=results_output
        )

        demo.load(
        fn=search_papers_b,
        inputs=[start_date, end_date],
        outputs=[page_buttons, status_output, results_output, page_buttons],
        scroll_to_output=False
    )

    with gr.Tab('All', id='all'):    
        with gr.Row():
            default_start_date = datetime.now() - timedelta(days=30)
            default_end_date = datetime.now()
            start_date = Calendar(value=default_start_date, label="📅 Start Date")
            end_date = Calendar(value=default_end_date, label="📅 End Date")
    
        search_btn = gr.Button("🔍 Search Papers", elem_id="search-btn", scale=2)
        status_output = gr.Textbox(label="Status", interactive=False)
        results_output = gr.HTML()
        page_buttons = gr.Radio(choices=[], label="📄 Pages", interactive=True, visible=False)
    
        search_btn.click(
            fn=search_papers_all,
            inputs=[start_date, end_date],
            outputs=[page_buttons, status_output, results_output, page_buttons]
        )
    
        page_buttons.change(
            fn=on_page_change_all,
            inputs=[page_buttons, start_date, end_date],
            outputs=results_output
        )

        demo.load(
        fn=search_papers_all,
        inputs=[start_date, end_date],
        outputs=[page_buttons, status_output, results_output, page_buttons],
        scroll_to_output=False
    )

    demo.load(None, js=js)
    

demo.launch(server_port=5001, server_name='0.0.0.0', root_path='/paper_aggregator', share=False)
