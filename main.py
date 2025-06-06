import os
import markdown
import shutil
from jinja2 import Environment, FileSystemLoader

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))

def render_markdown_file(md_path, template_name, output_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    html_content = markdown.markdown(md_content, extensions=["fenced_code", "codehilite"])
    template = env.get_template(template_name)
    output = template.render(content=html_content)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

# Render home page
render_markdown_file('content/home.md', 'page.html', 'docs/index.html')

# Render resume page
render_markdown_file('content/resume.md', 'page.html', 'docs/resume.html')


# Render blog posts
blog_dir = 'content/blog'
output_blog_dir = 'docs/blog'
os.makedirs(output_blog_dir, exist_ok=True)
blog_posts = []


for filename in os.listdir(blog_dir):
    if filename.endswith('.md'):
        post_name = filename[:-3]
        input_path = os.path.join(blog_dir, filename)
        output_path = os.path.join(output_blog_dir, f'{post_name}.html')
        render_markdown_file(input_path, 'blog_post.html', output_path)

        blog_posts.append({
            "title": post_name.replace('-', ' ').title(),
            "link": f'blog/{post_name}.html'
        })
    else : 
        print("Nothing to do 😭")
print("Blog posts found 😁")

# Generate blog index page

index_template = env.get_template('blog_index.html')
index_output = index_template.render(posts = blog_posts)
with open('docs/blog/index.html', 'w', encoding='utf-8') as f:
    f.write(index_output)
print("✅ Rendered to output file")

# Copy css file for access
# Define source and destination paths
source_path = 'static/style.css'
destination_path = 'docs/static/style.css'

# Ensure the output directory exists
os.makedirs('docs/static', exist_ok=True)

# Copy the file
shutil.copy(source_path, destination_path)

print(f"Copied '{source_path}' to '{destination_path}'")
