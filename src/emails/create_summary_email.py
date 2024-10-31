import json
import os
import sys
sys.path.append("\\".join(os.getcwd().split("\\")[:-1]))
import mongo_script
import logging
import datetime

def create_email():

    date_today = str(datetime.date.today())
    # date_today = '2024-10-29'
    try:
        json_data = mongo_script.retrieve_from_summary_db(date_today)
    except Exception as e:
        logging.info("Data is not scrapped properly.")
        logging.info(f"Error: {e}")

    if json_data is None:
        raise ValueError("Json of summaries is not found in MongoDB")
    # Constructing the HTML content
    html_content = """
    <html>
    <head>
        <style>
            body {
                text-align: justify; /* Justify all text in the body */
            }
        </style>
    </head>
    <body>
        <h3>Hi Pavilion Post Family,</h3>
        <p>Today's updates from the cricket world are:</p>
    """

    # Loop through the JSON data to create headings and bullet points, first will be the object so ignoring it
    first_id = False
    for section, updates in json_data.items():
        if not first_id:
            first_id=True
            continue

        if section=='latest_news_section':
            section = "Latest News"
        if section=='match_details':
            section = "Match Details"

        html_content += f"<h3>{section}</h3><ul>"
        for update in updates:
            title = list(update.keys())[0]
            story = update[title]
            html_content += f"<p><strong>{title}:</strong> {story}</p>"
        html_content += "</ul>"

    html_content += """
    <p>Hope you enjoyed the updates. We will keep you posted about the new happenings.</p>
    <p>Until then, Bye Bye</p>
    <p>Best Regards,<br>Anurag - The Pavilion Post Team</p>
    </body>
    </html>
    """

    with open('C:\\Users\\anuch\\Downloads\\Github\\cricket-updates\\data\\check_data.html',"w") as file:
        file.write(html_content)

    return html_content