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
        "SQL": "#336791",
        "mySQL": "#336791",
        "TypeScript": "#007ACC",
        "JavaScript": "#F7D35B",
        "HTML": "#E34F26",
        "C++": "#00599C",
        "CSS": "#2DA2D5",
        "React": "#61DAFB",
        "Duck DB": "#F8E7A4",
        "R": "#276DC3",
        "GO": "#00ADD8",
        "P4": "#000000"  # Example color for P4
    }

    software_colors = {
        "Bloomberg": "#00000F",
        "Finance": "#4F8A79",
        "Statistics": "#B38E8F",
        "Linux": "#000000",
        "Object Oriented Programming": "#FFC107",
        "Git": "#F05032",
        "Pandas": "#150458",
        "Microsoft Office": "#F25022",
        "jQuery": "#0769AD",
        "Rest API": "#67C4D8",
        "FAST API": "#00D1FF",
        "AWS": "#FF9900",
        "GCP": "#EA4335",
        "Docker": "#0DB7ED",
        "TensorFlow": "#FF6F00",
        "PyTorch": "#EE4C2C",
        "PyBullet": "#28A745",
        "Wireshark": "#339933",
        "Nix": "#7E8C8D",
        "Flask": "#000000",
        "Ajax": "#0F7BC2",
        "Streamlit": "#FD4145",
        "Terraform": "#7C3AED",
        "Yale": "#00356B",
        "IBM": "#1565F8",
        "Cloud": "#66DAD7",
        "Certificate": "#C8C390"
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
        color_code = "#0AFFFF"
    elif tag == "Frontend":
        color_code = "#DC143C"
    elif tag == "Backend":
        color_code = "#FF8C00"
    elif tag == "Database":
        color_code = "#FFD700"
    elif tag == "Mobile":
        color_code = "#FFFFF0"
    elif tag == "Natural-Language-Processing":
        color_code= "#00FF00"
    elif tag == "Machine-Learning":
        color_code= "#FFFFE0"
    elif tag == "Computer-Vision":
        color_code= "#FFFACD"
    elif tag == "Robotics":
        color_code= "#ADD8E6"
    elif tag == "Research":
        color_code= "#9370DB"
    else:
        color_code = "#BEE7FE"  # Default color for unknown tags
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