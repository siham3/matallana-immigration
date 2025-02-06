import pandas as pd
import os
from bs4 import BeautifulSoup 

def generate_service_pages(csv_file, template_file):
    # Read the CSV file, replacing NaN with empty strings
    df = pd.read_csv(csv_file).fillna("")  

    # Read the HTML template
    with open(template_file, 'r', encoding='utf-8') as file:
        template_html = file.read()
    
    # Create output directory if it doesn't exist
    os.makedirs('output_pages', exist_ok=True)
    
    # Generate a page for each service
    for _, row in df.iterrows():
        # Create a new BeautifulSoup object for each service
        soup = BeautifulSoup(template_html, 'html.parser')

        # Ensure values are strings
        row = row.astype(str)

        # Update page title
        soup.title.string = f"Matallana Immigration - {row['Name']}"
        
        # Update main content sections
        intro_content = soup.find('div', class_='intro-content')
        if intro_content:
            h1_tag = intro_content.find('h1', class_='heading-6')
            if h1_tag:
                h1_tag.string = row['Name']
            
            desc_tag = intro_content.find('div', class_='text-block-15')
            if desc_tag:
                desc_tag.string = row['Header Text']
        
        # Update main image
        main_image = soup.find('img', class_='image-13')
        if main_image and row['Main Image']:
            main_image['src'] = row['Main Image']
            main_image['alt'] = row['Name']
        
        # Update program details
        project_details = soup.find('div', class_='project-details-grid')
        if project_details:
            details_wraps = project_details.find_all('div', class_='details-wrap')

            if len(details_wraps) >= 3:
                # Ensure text is safely replaced
                details_wraps[0].find('div', class_='paragraph-light').string = str(row['Para 1'])
                details_wraps[1].find('div', class_='paragraph-light').string = str(row['Para 2'])
                details_wraps[2].find('div', class_='paragraph-light').string = str(row['Para 3'])
        
        # Update main body text
        main_content = soup.find('div', class_='paragraph-light', recursive=True)
        if main_content:
            main_content.clear()
            main_content.append(BeautifulSoup(str(row['Para 4']), 'html.parser'))
        
        # Save the generated page
        output_file = f"output_pages/{row['Slug']}.html"
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(str(soup))

# Usage
csv_file = 'matallana-immigration.csv'
template_file = 'detail_service.html'
generate_service_pages(csv_file, template_file)