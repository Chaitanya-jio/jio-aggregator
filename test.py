import gradio as gr
 
def home():
    return "Welcome to Home!"
 
def settings():
    return "Settings Page"
 
with gr.Blocks() as demo:
    with gr.Tabs() as tabs:
        with gr.Tab("Home", id="home"):
            home_output = gr.Textbox(value=home(), interactive=False)
        with gr.Tab("Settings", id="settings"):
            settings_output = gr.Textbox(value=settings(), interactive=False)
 
    demo.load(None, js="""
        () => {
            const urlParams = new URLSearchParams(window.location.search);
            const tab = urlParams.get("tab"); // e.g. ?tab=settings
            if (tab) {
                // Find tab button and click it
                const tabBtn = [...document.querySelectorAll('[role=tab]')]
                    .find(el => el.innerText.toLowerCase() === tab.toLowerCase());
                if (tabBtn) tabBtn.click();
            }
        }
    """)
 
demo.launch()