import gradio as gr
from gradio_calendar import Calendar 
from datetime import datetime, timedelta
import os
from pathlib import Path
from utils.wildfire import search_papers_w, on_page_change_w
from utils.quantum import search_papers_q, on_page_change_q
from utils.ai import search_papers_ai, on_page_change_ai
from utils.blockchain import search_papers_b, on_page_change_b
from utils.all import search_papers_all, on_page_change_all

# Tab switching JavaScript
tab_switching_js = """
() => {
  try {
    var params = new URLSearchParams(window.location.search);
    var wanted = params.get("tab");
    if (!wanted) return;

    console.log("🎯 Attempting to switch to tab: " + wanted);

    // Simple tab mapping
    var tabMap = {
      wildfire: "Wildfire prediction and forecasting using Deep learning",
      quantum_computing: "Quantum Computing", 
      ai: "Artificial Intelligence",
      web3_blockchain: "Web3 and Blockchain",
      web3: "Web3 and Blockchain",
      all: "All"
    };

    var targetLabel = tabMap[wanted];
    if (!targetLabel) {
      console.log("❌ Unknown tab parameter: " + wanted);
      return;
    }

    console.log("🔍 Looking for tab: " + targetLabel);

    // Enhanced tab finder with multiple selectors
    var findAndClickTab = function() {
      console.log("🔍 Searching for tabs with multiple selectors...");
      
      // Try multiple selectors for Gradio tabs
      var selectors = [
        'button[role="tab"]',
        '[role="tab"]', 
        'button.tab-nav',
        '.tab-nav button',
        'button:has-text("' + targetLabel + '")',
        'button'
      ];
      
      var allButtons = [];
      selectors.forEach(function(selector) {
        try {
          var buttons = Array.from(document.querySelectorAll(selector));
          allButtons = allButtons.concat(buttons);
          console.log("Selector '" + selector + "' found " + buttons.length + " elements");
        } catch (e) {
          console.log("Selector '" + selector + "' failed: " + e.message);
        }
      });
      
      // Remove duplicates
      allButtons = allButtons.filter(function(item, index) {
        return allButtons.indexOf(item) === index;
      });
      
      console.log("Total unique buttons/tabs found: " + allButtons.length);
      
      // Log all available tab texts for debugging
      console.log("Available tab texts: [" + 
        allButtons.map(function(btn) { 
          return '"' + (btn.innerText ? btn.innerText.trim() : btn.textContent ? btn.textContent.trim() : 'no-text') + '"'; 
        }).join(', ') + "]"
      );
      
      // Try exact match first
      var tabButton = allButtons.find(function(btn) {
        var text = btn.innerText || btn.textContent || '';
        return text.trim() === targetLabel;
      });
      
      // Try keyword match if exact fails
      if (!tabButton) {
        console.log("🔄 Exact match failed, trying keyword matching...");
        tabButton = allButtons.find(function(btn) {
          var text = (btn.innerText || btn.textContent || '').toLowerCase();
          if (wanted === 'quantum_computing' && text.includes('quantum')) return true;
          if (wanted === 'ai' && text.includes('artificial')) return true;
          if (wanted === 'web3' && (text.includes('web3') || text.includes('blockchain'))) return true;
          if (wanted === 'wildfire' && text.includes('wildfire')) return true;
          if (wanted === 'all' && text.trim() === 'all') return true;
          return false;
        });
      }
      
      if (tabButton) {
        console.log("✅ Found tab: " + (tabButton.innerText || tabButton.textContent).trim());
        console.log("🖱️ Clicking tab...");
        
        // Try multiple click methods
        try {
          tabButton.click();
          console.log("✅ Standard click executed");
        } catch (e) {
          console.log("❌ Standard click failed: " + e.message);
          try {
            tabButton.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
            console.log("✅ MouseEvent click executed");
          } catch (e2) {
            console.log("❌ MouseEvent click failed: " + e2.message);
          }
        }
        
        return true;
      }

      console.log("❌ Tab '" + targetLabel + "' not found in " + allButtons.length + " buttons");
      return false;
    };

    // Wait 2 seconds then try to find and click tab, with retries
    console.log("⏳ Waiting 2 seconds for page to load...");
    
    var attempts = 0;
    var maxAttempts = 3;
    
    var tryTabSwitch = function() {
      attempts++;
      console.log("🔄 Attempt " + attempts + "/" + maxAttempts + " to find and click tab");
      
      if (findAndClickTab()) {
        console.log("🎉 Success on attempt " + attempts + "!");
        return;
      }
      
      if (attempts < maxAttempts) {
        console.log("⏳ Retrying in 1 second...");
        tryTabSwitch();
      } else {
        console.log("❌ Failed after " + maxAttempts + " attempts");
      }
    };
    tryTabSwitch();

  } catch (e) {
    console.error("❌ Tab switching error:", e);
  }
}
"""

# Footer loading JavaScript
footer_loading_js = """
() => {
  try {
    console.log("📄 Footer loader initialized");
    
    // Load footer after 2 seconds
    setTimeout(function() {
        console.log("⏳ Loading footer after 2 seconds...");
        
        var footerPlaceholder = document.getElementById('footer-placeholder');
        if (footerPlaceholder) {
            footerPlaceholder.innerHTML = `
                <footer class="custom-footer">
                    <div class="footer-content">
                        <div class="footer-logo">
                            <img src="https://moonshotmatter.com/wp-content/uploads/2025/09/Screenshot-2025-09-05-at-2.58.24%E2%80%AFPM.png" 
                                 alt="MoonShotMatter Logo" class="footer-logo-img">
                        </div>
                        <div class="footer-nav">
                            <div class="footer-section">
                                <h4>Menu</h4>
                                <ul>
                                    <li><a href="https://www.moonshotmatter.com">Home</a></li>
                                    <li><a href="https://research.moonshotmatter.com">Research</a></li>
                                    <li><a href="https://trends.moonshotmatter.com">Trends</a></li>
                                    <li><a href="https://blog.moonshotmatter.com">Blog</a></li>
                                    <li><a href="https://moonshotmatter.com/company/contact-us/">Contact us</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="footer-bottom">
                        <p>©2025 MoonShotMatter, All Rights Reserved.</p>
                    </div>
                </footer>
            `;
            console.log("✅ Footer loaded successfully!");
        } else {
            console.log("❌ Footer placeholder not found");
        }
    }, 2000);
    
  } catch (e) {
    console.error("❌ Footer loading error:", e);
  }
}
"""


with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="orange")
) as demo:
    
    # Inject custom CSS at the bottom to override all default styles
    css_content = ""
    try:
        with open("static/custom.css", "r") as f:
            css_content = f.read()
    except FileNotFoundError:
        print("Warning: static/custom.css not found. Using default styling.")
    
    if css_content:
        gr.HTML(f"""
        <style id="custom-css-override">
        {css_content}
        </style>
        """)

    # Moonshot Matter Inspired Header
    gr.HTML("""
        <div class="header-container">
            <div class="header-content">
                <div class="logo-container">
                    <img src="https://moonshotmatter.com/wp-content/uploads/2025/09/Screenshot-2025-09-05-at-2.58.24%E2%80%AFPM.png" 
                         alt="Research Aggregator Logo" class="logo-img">
                    <div>
                        <!--div style="color: #fbbf24; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">RESEARCH PLATFORM</div-->
                        <!--h1 class="header-title">Research Insights</h1-->
                        <!--p class="header-subtitle">Industry-leading analysis across frontier technologies and next-gen research sectors.</p-->
                    </div>
                </div>
            </div>
        </div>
    """)
    
    with gr.Tab('Wildfire prediction and forecasting using Deep learning', id='wildfire'):
        with gr.Group(elem_classes=["search-container"]):
            with gr.Row():
                default_start_date = datetime.now() - timedelta(days=30)
                default_end_date = datetime.now()
                start_date = Calendar(value=default_start_date, label="📅 Start Date")
                end_date = Calendar(value=default_end_date, label="📅 End Date")
                search_btn = gr.Button("🔍 Search Papers", elem_classes=["search-btn"], scale=1)
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
        with gr.Group(elem_classes=["search-container"]):
            with gr.Row():
                default_start_date = datetime.now() - timedelta(days=30)
                default_end_date = datetime.now()
                start_date = Calendar(value=default_start_date, label="📅 Start Date")
                end_date = Calendar(value=default_end_date, label="📅 End Date")
                search_btn = gr.Button("🔍 Search Papers", elem_classes=["search-btn"], scale=1)
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
        with gr.Group(elem_classes=["search-container"]):
            with gr.Row():
                default_start_date = datetime.now() - timedelta(days=30)
                default_end_date = datetime.now()
                start_date = Calendar(value=default_start_date, label="📅 Start Date")
                end_date = Calendar(value=default_end_date, label="📅 End Date")
                search_btn = gr.Button("🔍 Search Papers", elem_classes=["search-btn"], scale=1)
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
        with gr.Group(elem_classes=["search-container"]):
            with gr.Row():
                default_start_date = datetime.now() - timedelta(days=30)
                default_end_date = datetime.now()
                start_date = Calendar(value=default_start_date, label="📅 Start Date")
                end_date = Calendar(value=default_end_date, label="📅 End Date")
                search_btn = gr.Button("🔍 Search Papers", elem_classes=["search-btn"], scale=1)
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
        with gr.Group(elem_classes=["search-container"]):
            with gr.Row():
                default_start_date = datetime.now() - timedelta(days=30)
                default_end_date = datetime.now()
                start_date = Calendar(value=default_start_date, label="📅 Start Date")
                end_date = Calendar(value=default_end_date, label="📅 End Date")
                search_btn = gr.Button("🔍 Search Papers", elem_classes=["search-btn"], scale=1)
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

    # Footer placeholder - will be loaded via JavaScript after 2 seconds
    gr.HTML('<div id="footer-placeholder"></div>')

    # Load tab switching JavaScript
    demo.load(None, js=tab_switching_js)
    
    # Load footer loading JavaScript  
    demo.load(None, js=footer_loading_js)
    
    # Load CSS and layout management JavaScript
    demo.load(None, js="""
    // Enhanced CSS and layout management
    var ensureCustomStyling = function() {
        // Force full width and remove padding on load, but preserve tabs
        var containers = document.querySelectorAll('.gradio-container, .app, .fillable, .main-wrap, .wrap, .contain, .main, .block, .form, div[data-testid="block-container"]');
        containers.forEach(function(el) {
            el.style.maxWidth = 'none';
            el.style.width = '100%';
            el.style.padding = '0';
            el.style.margin = '0';
        });
        
        // Ensure tabs are visible and functional
        var tabs = document.querySelectorAll('[role="tablist"], [role="tab"], [role="tabpanel"], .tabitem');
        tabs.forEach(function(tab) {
            tab.style.display = tab.getAttribute('role') === 'tablist' ? 'flex' : 'block';
            tab.style.visibility = 'visible';
        });
        
        // Ensure custom CSS takes priority by moving it to the end
        var customCSS = document.getElementById('custom-css-override');
        if (customCSS) {
            document.head.appendChild(customCSS);
        }
        
        // Hide Gradio default footer and social media elements
        var gradioFooter = document.querySelector('footer');
        if (gradioFooter && !gradioFooter.classList.contains('custom-footer')) {
            gradioFooter.style.display = 'none';
        }
        
        // Remove any social media links or go-to-top buttons that might be added by Gradio
        var socialElements = document.querySelectorAll('a[href*="twitter"], a[href*="linkedin"], a[href*="youtube"], a[href*="instagram"], a[href*="facebook"], .scroll-to-top, .go-to-top');
        socialElements.forEach(function(el) { el.style.display = 'none'; });
        
        // Add additional runtime overrides that come after all other CSS
        var runtimeStyle = document.getElementById('runtime-overrides');
        if (!runtimeStyle) {
            runtimeStyle = document.createElement('style');
            runtimeStyle.id = 'runtime-overrides';
            runtimeStyle.innerHTML = '/* Runtime CSS overrides - highest priority */ .fillable.svelte-16faplo.svelte-16faplo:not(.fill_width) { max-width: none !important; width: 100% !important; padding: 0 !important; } .gradio-container, .app, .fillable, .main-wrap, .wrap, .contain, .main, .block, .form { max-width: none !important; width: 100% !important; padding: 0 !important; margin: 0 !important; } [role="tablist"] { display: flex !important; visibility: visible !important; } [role="tab"] { display: inline-flex !important; visibility: visible !important; } [role="tabpanel"] { display: block !important; visibility: visible !important; } :root { --size-4: 0px !important; --size-8: 0px !important; --spacing-sm: 0px !important; --spacing-md: 0px !important; --spacing-lg: 0px !important; } footer:not(.custom-footer) { display: none !important; } a[href*="twitter"], a[href*="linkedin"], a[href*="youtube"], a[href*="instagram"], a[href*="facebook"], .scroll-to-top, .go-to-top, .social-links, .social-media { display: none !important; } body * { box-sizing: border-box; }';
            document.head.appendChild(runtimeStyle);
        }
        
        console.log('Custom styling applied and prioritized');
    }
    
    // Run styling function multiple times to ensure it takes effect
    ensureCustomStyling();
    window.addEventListener('resize', ensureCustomStyling);
    setTimeout(ensureCustomStyling, 500);   // Early catch
    setTimeout(ensureCustomStyling, 1000);  // Standard timing
    setTimeout(ensureCustomStyling, 2000);  // Late catch
    setTimeout(ensureCustomStyling, 5000);  // Final override
    
    // Monitor for DOM changes and reapply styling
    var observer = new MutationObserver(function() {
        setTimeout(ensureCustomStyling, 100);
    });
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['class', 'style']
    });
    """)
    
    # Set the page title and favicon at runtime to 'moonshotmatter'
    demo.load(None, js="""
    () => {
        try {
            document.title = "Moonshotmatter";
            var link = document.querySelector("link[rel*='icon']") || document.createElement('link');
            link.type = 'image/png';
            link.rel = 'icon';
            link.href = 'https://moonshotmatter.com/wp-content/uploads/2025/09/Screenshot-2025-09-05-at-2.58.24%E2%80%AFPM.png';
            if (!document.querySelector("link[rel*='icon']")) document.head.appendChild(link);
        } catch(e) { console.error('favicon/title set error', e); }
    }
    """)


# Ensure static directory exists
static_dir = Path("static")
static_dir.mkdir(exist_ok=True)

demo.launch(
    server_port=5001, 
    server_name='0.0.0.0', 
    root_path='/paper_aggregator', 
    share=False,
    show_api=False,
    favicon_path="static/favicon.ico" if os.path.exists("static/favicon.ico") else None
)
