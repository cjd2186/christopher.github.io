import os
import json
from jinja2 import Environment, FileSystemLoader

# Load JSON data
with open('static/json/data.json', 'r') as file:
    data = json.load(file)

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))
index_template = env.get_template('index.html')
project_template = env.get_template('project.html')
job_template = env.get_template('job.html')

# Ensure the output directory exists
output_dir = 'templates/pages'
os.makedirs(output_dir, exist_ok=True)

# Define the color generation function
def generate_color(tag):
    with open('static/json/colors.json', 'r') as file:
        colors = json.load(file)
    if tag in colors.keys():
        return colors[tag]
    else:
        return "#BEE7FE"

def get_tag_colors(data):
    tag_colors = {}

    def process_items(items):
        for item in items:
            if item:  # Ensure the item is not empty
                for tag in item.get('tags', []):
                    if tag not in tag_colors:
                        tag_colors[tag] = generate_color(tag)
    
    # Process projects
    for category, subcategories in data['projects'].items():
        for subcategory, items in subcategories.items():
            process_items(items)
    
    # Process jobs
    for role_category, roles in data['jobs']['roles'].items():
        process_items(roles)

    for cert in data['certs']:
        print(cert)
        if cert:  # Ensure the item is not empty
            for tag in cert['tags']:
                if tag not in tag_colors:
                    tag_colors[tag] = generate_color(tag)
    return tag_colors

# Generate tag colors
tag_colors = get_tag_colors(data)

# Prepare the context for index.html
context = {
    'projects': data['projects'],
    'jobs': data['jobs'],
    'certs': data['certs'],
    'tag_colors': tag_colors
}

# Render and save index.html
index_html_content = index_template.render(context)
with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as file:
    file.write(index_html_content)
    print("index.html has been created.")

# Generate individual project pages
for category, categories in data['projects'].items():
    for subcategory, projects in categories.items():
        for project in projects:
            project_context = {
                'project': project,
                'tag_colors': tag_colors
            }
            project_html_content = project_template.render(project_context)
            project_output_path = os.path.join(output_dir, f"{project['name']}.html")
            with open(project_output_path, 'w', encoding='utf-8') as file:
                file.write(project_html_content)
                print(f"{project['name']}.html has been created.")

# Generate individual job pages
for category, categories in data['jobs'].items():
    for subcategory, jobs in categories.items():
        for job in jobs:
            job_context = {
                'jobs': job,
                'tag_colors': tag_colors
            }
            job_html_content = job_template.render(job_context)
            job_output_path = os.path.join(output_dir, f"{job['company'].replace(' ', '_')}.html")
            with open(job_output_path, 'w', encoding='utf-8') as file:
                file.write(job_html_content)
                print(f"{job['company'].replace(' ', '_')}.html has been created.")