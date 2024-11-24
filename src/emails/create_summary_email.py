import json
import os
import sys
sys.path.append("\\".join(os.getcwd().split("\\")[:-1]))
import src.mongo_script as ms
import logging
from datetime import datetime
from datetime import date

def generate_news_html(news_items):
    news_html = ""
    for news in news_items:
        title = list(news.keys())[0]
        story = news[title]
        news_html += f"""
                <div class="news-item">
                    <h3 class="news-title">{title}</h3>
                    <div class="news-content">
                        {story}
                    </div>
                </div>
        """
    return news_html

def generate_matches_html(matches):
    matches_html = ""
    for match in matches:
        title = list(match.keys())[0]
        story = match[title]
        matches_html += f"""
                <div class="match-item">
                    <h3 class="match-title">{title}</h3>
                    <div class="match-details">
                        {story}
                    </div>
                </div>
        """
    return matches_html
def generate_email_html(news_data, match_data):
    # Get current date and year
    current_date = datetime.now().strftime("%B %d, %Y")
    current_year = datetime.now().year
    
    # Generate HTML for news and matches sections
    news_html = generate_news_html(news_data)
    matches_html = generate_matches_html(match_data)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ 
                margin: 0; 
                padding: 0; 
                font-family: Arial, sans-serif;
                background-color: #f3f4f6;
            }}
            
            .container {{ 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 20px; 
            }}
            
            .header {{
                background-color: #2563eb;
                color: white;
                padding: 24px;
                border-radius: 8px 8px 0 0;
                text-align: center;
            }}
            
            .grid-container {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 20px;
                padding: 20px;
                background-color: #f8fafc;
                border-radius: 0 0 8px 8px;
            }}
            
            @media (min-width: 768px) {{
                .grid-container {{
                    grid-template-columns: 1fr 1fr;
                }}
            }}
            
            .section {{
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            
            .section-title {{
                color: #1e40af;
                font-size: 24px;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #e5e7eb;
            }}
            
            .news-item {{
                background-color: #f8fafc;
                margin-bottom: 20px;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #2563eb;
            }}
            
            .news-title {{
                color: #1e3a8a;
                font-size: 18px;
                margin-bottom: 10px;
            }}
            
            .news-content {{
                color: #374151;
                line-height: 1.5;
            }}
            
            .match-item {{
                background-color: #f8fafc;
                margin-bottom: 20px;
                padding: 15px;
                border-radius: 8px;
            }}
            
            .match-title {{
                color: #1e3a8a;
                font-size: 18px;
                margin-bottom: 10px;
            }}
            
            .match-details {{
                background-color: #eff6ff;
                padding: 10px;
                border-radius: 6px;
                margin-bottom: 10px;
            }}
            
            .footer {{
                text-align: center;
                padding: 20px;
                color: #6b7280;
                font-size: 14px;
                background-color: #f8fafc;
                border-radius: 8px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Cricket Daily Digest</h1>
                <p>{current_date}</p>
            </div>
            
            <div class="grid-container">
                <div class="section">
                    <h2 class="section-title">Latest News</h2>
                    {news_html}
                </div>
                
                <div class="section">
                    <h2 class="section-title">Match Updates</h2>
                    {matches_html}
                </div>
            </div>
            
            <div class="footer">
                <p>Stay tuned for more cricket updates tomorrow!</p>
                <p>&copy; {current_year} Pavilion Post </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def create_email():

    date_today = str(date.today())
    # date_today = '2024-11-23'
    try:
        json_data = ms.retrieve_from_summary_db(date_today)
    except Exception as e:
        logging.info("Data is not scrapped properly.")
        logging.info(f"Error: {e}")

    if json_data is None:
        raise ValueError("Json of summaries is not found in MongoDB")
    
    # Generate HTML from JSON data
    html_content = generate_email_html(json_data['latest_news_section'], json_data['match_details'])
        
    # Save to file (optional)
    with open('cricket_newsletter.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    return html_content