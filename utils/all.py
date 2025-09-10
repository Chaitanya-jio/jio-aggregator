import gradio as gr
from utils.blockchain import count_papers as count_papers_b
from utils.blockchain import query_papers as query_papers_b
from utils.quantum import count_papers as count_papers_q
from utils.quantum import query_papers as query_papers_q
from utils.wildfire import count_papers as count_papers_w
from utils.wildfire import query_papers as query_papers_w
from utils.ai import count_papers as count_papers_a
from utils.ai import query_papers as query_papers_a

def display_results(start_date, end_date, page):
    limit = 10
    offset = (page - 1) * limit

    # Collect everything without pagination
    papers = query_papers_b(start_date, end_date, limit=None, offset=None) + \
             query_papers_q(start_date, end_date, limit=None, offset=None) + \
             query_papers_w(start_date, end_date, limit=None, offset=None) + \
             query_papers_a(start_date, end_date, limit=None, offset=None)

    # Sort by published date (newest first)
    papers.sort(key=lambda x: x[2], reverse=True)

    # Apply pagination globally
    papers = papers[offset: offset + limit]
    if not papers:
        return """
        <p style="
            font-family: 'Inter', sans-serif;
            font-size: 1.2em;
            text-align: center;
            color: #64748b;
            margin-top: 60px;
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        ">
            <span style="font-weight: 700; font-size: 2em; color:#ea580c;">No</span> papers found for the selected date range.
        </p>
        """
 
    formatted_html = ""
    for title, authors, published, updated, summary, link_alt, link_pdf in papers:
        submitted_date = published[:10]  # Only YYYY-MM-DD
        
        if link_pdf:
            link_pdf = "https" + link_pdf[4:]
            link_alt = "https" + link_alt[4:]
            pdf_html = f'''
            <iframe src="{link_pdf}"
                    width="85%" height="300px" style="border:1px solid #ccc; border-radius:8px;">
            </iframe>
            '''
        else:
            pdf_html = "<p>No PDF Available</p>"
 
        formatted_html += f"""
        <div class="paper-card" style="display: flex; gap: 32px;">
            <div style="flex: 1; min-width: 0;">
                <a href="{link_alt}" target="_blank" class="paper-title">{title}</a>
                <div class="paper-meta">
                    <strong>Authors:</strong> {authors}
                </div>
                <div class="paper-meta">
                    <strong>Submitted:</strong> {submitted_date}
                </div>
                <div class="paper-summary">
                    <strong>Summary:</strong> {summary}
                </div>
            </div>
            <div style="width: 450px;" class="pdf-container">
                {pdf_html}
            </div>
        </div>
        """
    return formatted_html
 
def on_page_change_all(selected_page, start_date, end_date):
    page = int(selected_page)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    html = display_results(start_date_str, end_date_str, page)
    return html

def search_papers_all(start_date, end_date):
    try:
        # Convert to string format yyyy-mm-dd for DB queries
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
    except Exception:
        return gr.update(visible=False), "Invalid date format. Use YYYY-MM-DD.", "", gr.update(visible=False)
 
    total_results = count_papers_b(start_date_str, end_date_str) + \
            count_papers_q(start_date_str, end_date_str) + \
            count_papers_w(start_date_str, end_date_str) + \
            count_papers_a(start_date_str, end_date_str)
    
    if total_results == 0:
        return gr.update(visible=False), "", display_results(start_date_str, end_date_str, 1), gr.update(visible=False)
 
    max_pages = max((total_results + 9) // 10, 1)
    html = display_results(start_date_str, end_date_str, 1)
 
    return (
        gr.update(visible=True),
        f"Found {total_results} papers.",
        html,
        gr.update(visible=True, choices=[str(i) for i in range(1, max_pages + 1)], value="1")
    )
 