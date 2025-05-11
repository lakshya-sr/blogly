from flask import Flask, send_from_directory, abort, render_template, request, redirect
import os
import markdown

app = Flask("Blogly")

# Define the directory where your HTML pages are stored
BLOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blogs')

@app.route('/create_blog')
def create_blog():
    return render_template('create_blog.html')

@app.route('/submit_markdown', methods=['POST'])
def submit_markdown():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()

    if not title or not content:
        return "Title and content are required.", 400

    # Convert Markdown to HTML
    html_content = markdown.markdown(content)

    # Simple file-safe slug
    slug = title.lower().replace(' ', '_').replace('.', '').replace('/', '')
    filename = os.path.join(BLOG_DIR, f"{slug}.html")

    # Save HTML to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"<h1>{title}</h1>\n{html_content}")

    return redirect(f"/{slug}")

@app.route('/<page_name>')
def serve_page(page_name):
    # Append .html if not included
    if not page_name.endswith('.html'):
        page_name += '.html'
    try:
        return send_from_directory(BLOG_DIR, page_name)
    except FileNotFoundError:
        abort(404)

@app.route('/')
def home():
    return render_template('index.html', pages=get_pages())

def get_pages(path="blogs"):
    files = [i for i in os.scandir(path=path) if i.is_file()]
    return [i.name for i in files]

if __name__ == '__main__':
    app.run(debug=True)
