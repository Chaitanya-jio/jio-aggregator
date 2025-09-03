import sqlite3
DB_FILENAME = 'arxiv_ai_database.db'
import gradio as gr

def query_papers(start_date, end_date, limit=10, offset=0):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    query = '''
    SELECT title, authors, published, updated, generated_summary, link_alternate, link_pdf
    FROM arxiv_papers
    WHERE DATE(substr(published, 1, 10)) BETWEEN ? AND ?
    ORDER BY published DESC
    '''
    
    params = [start_date, end_date]
    if limit is not None and offset is not None:
        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    conn.close()
    return results
 
def count_papers(start_date, end_date):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    query = '''
        SELECT COUNT(*)
        FROM arxiv_papers
        WHERE DATE(substr(published, 1, 10)) BETWEEN ? AND ?
    '''
    cursor.execute(query, (start_date, end_date))
    total = cursor.fetchone()[0]
    conn.close()
    return total
 
def display_results(start_date, end_date, page):
    limit = 10
    offset = (page - 1) * 10
    papers = query_papers(start_date, end_date, limit=limit, offset=offset)
    if not papers:
        return """
        <p style="
            font-family: 'Roboto', sans-serif;
            font-size: 1.2em;
            text-align: center;
            color: #555;
            margin-top: 40px;
        ">
            <span style="font-weight: 700; font-size: 2em; color:#6f42c1;">No</span> papers found for the selected date range.
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
        <div style="
            display: flex; background: #f2f2f9; border: 2px solid #c4c4ff;
            padding: 15px; margin-bottom: 20px; border-radius: 10px;
            font-family: 'Roboto', sans-serif;
        ">
            <div style="width: 65%; padding-right: 15px;">
                <h2 style="color: #2a2a75; margin-bottom: 10px; font-size: 1.6em;">
                    <a href="{link_alt}" target="_blank" style="text-decoration:none; color:#2a2a75;">{title}</a>
                </h2>
                <p style="margin-bottom: 6px;"><strong>Authors:</strong> {authors}</p>
                <p style="margin-bottom: 6px;"><strong>Submitted:</strong> {submitted_date}</p>
                <p style="margin-bottom: 6px;"><strong>Summary:</strong> {summary}</p>
            </div>
            <div style="width: 35%; display: flex; justify-content: flex-end;">
                {pdf_html}
            </div>
        </div>
        """
    return formatted_html
 
def on_page_change_ai(selected_page, start_date, end_date):
    page = int(selected_page)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')
    html = display_results(start_date_str, end_date_str, page)
    return html

def search_papers_ai(start_date, end_date):
    try:
        # Convert to string format yyyy-mm-dd for DB queries
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
    except Exception:
        return gr.update(visible=False), "Invalid date format. Use YYYY-MM-DD.", "", gr.update(visible=False)
 
    total_results = count_papers(start_date_str, end_date_str)
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
 