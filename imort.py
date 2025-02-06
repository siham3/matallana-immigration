import os

# Directory containing the service HTML files
services_dir = os.path.join(os.path.dirname(__file__), "output_pages")

# Base HTML template for links
link_template = '<a href="services/{filename}" class="dropdown-link-9 w-dropdown-link">{service_name}</a>'

# Generate links dynamically
service_links = []
for filename in os.listdir(services_dir):
    if filename.endswith(".html"):
        print("Found service:", filename)   
        # Generate service name from filename
        service_name = filename.replace("-", " ").replace(".html", "").title()
        # Append link to the list
        service_links.append(link_template.format(filename=filename, service_name=service_name))

# Combine links into a single string
service_links_html = "\n".join(service_links)

# Update index.html
with open("matallana-immigration.webflows/index.html", "r", encoding="utf-8") as file:
    index_html = file.read()

# Replace placeholder or existing services dropdown with new links
updated_html = index_html.replace(
    '<!-- Service Links Placeholder -->',
    service_links_html
)

# Write updated HTML back to file
with open("index.html", "w", encoding="utf-8") as file:
    file.write(updated_html)

print("Index.html updated with service links!")