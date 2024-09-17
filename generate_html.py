import os
import json
from jinja2 import Environment, FileSystemLoader
import collections 
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

    
# Prepare the context for index.html
context = {
    'projects': data['projects'],
    'jobs': data['jobs'],
    'certs': data['certs'],
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
            }
            job_html_content = job_template.render(job_context)
            job_output_path = os.path.join(output_dir, f"{job['company'].replace(' ', '_')}.html")
            with open(job_output_path, 'w', encoding='utf-8') as file:
                file.write(job_html_content)
                print(f"{job['company'].replace(' ', '_')}.html has been created.")

def count_tags(data):
    #get project tags
    tags=collections.defaultdict(int)
    for category, subcategories in data['projects'].items():
        for subcategory, items in subcategories.items():
            for item in items:
                for tag in item.get('tags', []):
                    tags[tag]+=1
    # Process jobs
    for role_category, roles in data['jobs']['roles'].items():
        for item in roles:
            for tag in item.get('tags', []):
                tags[tag]+=1

    for cert in data['certs']:
        if cert: 
            for tag in cert['tags']:
                tags[tag]+=1
    
    
    sorted_tags = dict(sorted(tags.items(), key=lambda item: (item[1], item[0])))
    with open("static/json/tags.json", 'w', encoding='utf-8') as file:
        json.dump(sorted_tags, file, ensure_ascii=False, indent=4)
        print("tags.json has been created")

count_tags(data)