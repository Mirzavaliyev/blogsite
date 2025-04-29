import os
import django
import urllib.parse

# Django sozlamalarini yuklash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')  # 'your_project' ni loyiha nomingizga o‘zgartiring
django.setup()

# Modelni import qilish
from main.models import Post  # 'your_app' ni ilova nomingizga o‘zgartiring

# Rasml
posts = Post.objects.all()
for post in posts:
    if '%' in post.image.name:
        decoded_name = urllib.parse.unquote(post.image.name)
        post.image.name = decoded_name
        post.save()
        print(f"Updated: {post.image.name}")