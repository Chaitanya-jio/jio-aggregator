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

# replace your js string with this:
js = """
function switchToTabFromURL() {
  try {
    const params = new URLSearchParams(window.location.search);
    const wanted = params.get("tab");
    if (!wanted) return;

    console.log(`Attempting to switch to tab: ${wanted}`);

    // map short keys -> actual tab labels shown in the UI
    const map = {
      wildfire: "Wildfire prediction and forecasting using Deep learning",
      quantum_computing: "Quantum Computing",
      ai: "Artificial Intelligence",
      web3_blockchain: "Web3 and Blockchain",
      web3: "Web3 and Blockchain",  // alias for web3_blockchain
      all: "All",
    };

    const wantedLabel = map[wanted] || wanted;
    console.log(`Looking for tab with label: "${wantedLabel}"`);

    // Wait for tabs to be ready
    const findAndClickTab = () => {
      const tabs = Array.from(document.querySelectorAll("[role='tab']"));
      console.log(`Found ${tabs.length} tabs:`, tabs.map(t => `"${t.innerText.trim()}"`));
      
      if (tabs.length === 0) {
        console.log("No tabs found, retrying...");
        return false;
      }

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

      if (btn) {
        btn.click();
        console.log(`✅ Successfully switched to tab: "${btn.innerText.trim()}" from URL parameter: ${wanted}`);
        return true;
      } else {
        console.log(`❌ Tab not found for URL parameter: ${wanted}`);
        console.log(`Available tabs:`, tabs.map(t => `"${t.innerText.trim()}"`));
        return false;
      }
    };

    // Try immediately
    if (findAndClickTab()) return;

    // If not found, retry with delays
    setTimeout(() => {
      if (findAndClickTab()) return;
      
      setTimeout(() => {
        findAndClickTab();
      }, 1000);
    }, 500);

  } catch (e) {
    console.log("tab init error", e);
  }
}

// Call the function immediately
switchToTabFromURL();

// Test function to verify all tab routes work
function testAllTabRoutes() {
  const testRoutes = [
    'wildfire',
    'quantum_computing', 
    'ai',
    'web3_blockchain',
    'web3',
    'all'
  ];
  
  console.log('🧪 Testing all tab routes...');
  testRoutes.forEach(route => {
    const params = new URLSearchParams();
    params.set('tab', route);
    console.log(`Testing route: ?tab=${route}`);
  });
}

// Function to update URL when tab is clicked
function updateURLOnTabChange() {
  try {
    const tabs = Array.from(document.querySelectorAll("[role='tab']"));
    
    // Reverse mapping: tab labels -> URL parameters
    const reverseMap = {
      "Wildfire prediction and forecasting using Deep learning": "wildfire",
      "Quantum Computing": "quantum_computing", 
      "Artificial Intelligence": "ai",
      "Web3 and Blockchain": "web3",
      "All": "all"
    };
    
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const tabText = tab.innerText.trim();
        const urlParam = reverseMap[tabText];
        
        if (urlParam) {
          const newUrl = new URL(window.location);
          newUrl.searchParams.set('tab', urlParam);
          window.history.replaceState({}, '', newUrl.toString());
          console.log(`Updated URL to: ${newUrl.toString()}`);
        }
      });
    });
  } catch (e) {
    console.log("URL update setup error", e);
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

    # Footer
    gr.HTML("""
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
    """)

    demo.load(None, js=js + """
    // Enhanced CSS and layout management
    function ensureCustomStyling() {
        // Force full width and remove padding on load, but preserve tabs
        const containers = document.querySelectorAll('.gradio-container, .app, .fillable, .main-wrap, .wrap, .contain, .main, .block, .form, div[data-testid="block-container"]');
        containers.forEach(el => {
            el.style.maxWidth = 'none';
            el.style.width = '100%';
            el.style.padding = '0';
            el.style.margin = '0';
        });
        
        // Ensure tabs are visible and functional
        const tabs = document.querySelectorAll('[role="tablist"], [role="tab"], [role="tabpanel"], .tabitem');
        tabs.forEach(tab => {
            tab.style.display = tab.getAttribute('role') === 'tablist' ? 'flex' : 'block';
            tab.style.visibility = 'visible';
        });
        
        // Ensure custom CSS takes priority by moving it to the end
        const customCSS = document.getElementById('custom-css-override');
        if (customCSS) {
            document.head.appendChild(customCSS);
        }
        
        // Hide Gradio default footer and social media elements
        const gradioFooter = document.querySelector('footer');
        if (gradioFooter && !gradioFooter.classList.contains('custom-footer')) {
            gradioFooter.style.display = 'none';
        }
        
        // Remove any social media links or go-to-top buttons that might be added by Gradio
        const socialElements = document.querySelectorAll('a[href*="twitter"], a[href*="linkedin"], a[href*="youtube"], a[href*="instagram"], a[href*="facebook"], .scroll-to-top, .go-to-top');
        socialElements.forEach(el => el.style.display = 'none');
        
        // Add additional runtime overrides that come after all other CSS
        let runtimeStyle = document.getElementById('runtime-overrides');
        if (!runtimeStyle) {
            runtimeStyle = document.createElement('style');
            runtimeStyle.id = 'runtime-overrides';
            runtimeStyle.innerHTML = `
                /* Runtime CSS overrides - highest priority */
                .fillable.svelte-16faplo.svelte-16faplo:not(.fill_width) {
                    max-width: none !important;
                    width: 100% !important;
                    padding: 0 !important;
                }
                .gradio-container, .app, .fillable, .main-wrap, .wrap, .contain, .main, .block, .form {
                    max-width: none !important;
                    width: 100% !important;
                    padding: 0 !important;
                    margin: 0 !important;
                }
                [role="tablist"] {
                    display: flex !important;
                    visibility: visible !important;
                }
                [role="tab"] {
                    display: inline-flex !important;
                    visibility: visible !important;
                }
                [role="tabpanel"] {
                    display: block !important;
                    visibility: visible !important;
                }
                :root {
                    --size-4: 0px !important;
                    --size-8: 0px !important;
                    --spacing-sm: 0px !important;
                    --spacing-md: 0px !important;
                    --spacing-lg: 0px !important;
                }
                
                /* Hide default Gradio footer and social elements */
                footer:not(.custom-footer) {
                    display: none !important;
                }
                
                a[href*="twitter"], a[href*="linkedin"], a[href*="youtube"], 
                a[href*="instagram"], a[href*="facebook"], 
                .scroll-to-top, .go-to-top,
                .social-links, .social-media {
                    display: none !important;
                }
                
                /* Ensure custom styles always override */
                body * {
                    box-sizing: border-box;
                }
            `;
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
    
    // Setup URL updating for tab changes
    setTimeout(updateURLOnTabChange, 1000);  // Setup after tabs are ready
    
    // Call tab switching function multiple times to ensure it works
    setTimeout(switchToTabFromURL, 500);   // Early attempt
    setTimeout(switchToTabFromURL, 1500);  // After tabs are ready
    setTimeout(switchToTabFromURL, 3000);  // Final attempt
    
    // Test tab routes after tabs are loaded (only in development)
    setTimeout(() => {
      if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        testAllTabRoutes();
      }
    }, 2000);
    
    // Monitor for DOM changes and reapply styling
    const observer = new MutationObserver(() => {
        setTimeout(ensureCustomStyling, 100);
        setTimeout(updateURLOnTabChange, 200);  // Re-setup URL updating after DOM changes
        setTimeout(switchToTabFromURL, 300);    // Re-check tab switching after DOM changes
    });
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['class', 'style']
    });
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
