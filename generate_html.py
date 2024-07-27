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
    lang_colors = {
        "Python": "#306998",
        "Java": "#007396",
        "C": "#00599C",
        "PostgreSQL": "#336791",
        "TypeScript": "#007ACC",
        "HTML": "#E34F26",
        "C++": "#00599C",
        "React": "#61DAFB",
        "Duck DB": "#F8E7A4",
        "R": "#276DC3",
        "GO": "#00ADD8",
        "P4": "#000000"  # Example color for P4
    }

    software_colors = {
        "Bloomberg": "#F8F8F8",
        "Linux": "#000000",
        "Object Oriented Programming": "#FFC107",
        "Git": "#F05032",
        "Pandas": "#150458",
        "Microsoft Office": "#F25022",
        "jQuery": "#0769AD",
        "REST": "#67C4D8",
        "FAST API": "#00D1FF",
        "AWS": "#FF9900",
        "GCP": "#4285F4",
        "Docker": "#0DB7ED",
        "TensorFlow": "#FF6F00",
        "PyTorch": "#EE4C2C",
        "PyBullet": "#28A745",
        "Wireshark": "#339933",
        "Nix": "#7E8C8D",
        "Flask": "#000000",
        "Terraform": "#7C3AED"
    }

    if tag in lang_colors:
        color_code = lang_colors[tag]
    elif tag in software_colors:
        color_code = software_colors[tag]
    elif tag == "Columbia":
        color_code = "#C4D8E2"
    elif tag == "Teamwork":
        color_code = "#4CAF50"
    elif tag == "Independent":
        color_code = "#FFFFFF"
    else:
        color_code = "#D3D3D3"  # Default color for unknown tags
    return color_code

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

    return tag_colors

# Generate tag colors
tag_colors = get_tag_colors(data)

# Prepare the context for index.html
context = {
    'projects': data['projects'],
    'jobs': data['jobs'],
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
                'job': job,
                'tag_colors': tag_colors
            }
            job_html_content = job_template.render(job_context)
            job_output_path = os.path.join(output_dir, f"{job['role'].replace(' ', '_')}.html")
            with open(job_output_path, 'w', encoding='utf-8') as file:
                file.write(job_html_content)
                print(f"{job['role'].replace(' ', '_')}.html has been created.")