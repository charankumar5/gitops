from flask import Flask, render_template_string
import docker

app = Flask(__name__)
client = docker.from_env()

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Docker Dashboard</title>
    <meta http-equiv="refresh" content="10">
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 40px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        h1, h2 { color: #333; }
    </style>
</head>
<body>
    <h1>Company Name</h1>

    <h2>Running Docker Containers</h2>
    <table>
        <tr><th>Container ID</th><th>Name</th><th>Image</th><th>Status</th></tr>
        {% for container in containers %}
        <tr>
            <td>{{ container.short_id }}</td>
            <td>{{ container.name }}</td>
            <td>{{ container.image.tags[0] if container.image.tags else container.image.short_id }}</td>
            <td>{{ container.status }}</td>
        </tr>
        {% endfor %}
    </table>

    <h2>Available Docker Images</h2>
    <table>
        <tr><th>Repository:Tag</th><th>Image ID</th><th>Size (MB)</th></tr>
        {% for image in images %}
        <tr>
            <td>
                {% if image.tags %}
                    {{ image.tags[0] }}
                {% else %}
                    <i>&lt;none&gt;</i>
                {% endif %}
            </td>
            <td>{{ image.short_id }}</td>
            <td>{{ "%.2f"|format(image.attrs['Size'] / 1024 / 1024) }}</td>
        </tr>
        {% endfor %}
    </table>

    <p>Page auto-refreshes every 10 seconds.</p>
</body>
</html>
'''

@app.route('/')
def home():
    containers = client.containers.list(all=True)
    images = client.images.list()
    return render_template_string(TEMPLATE, containers=containers, images=images)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
