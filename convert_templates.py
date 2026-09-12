import re
import os

TEMPLATES_DIR = "templates"
PAGES = [
    "about.html", "contact.html", "courses.html", "course-details.html",
    "events.html", "pricing.html", "trainers.html", "starter-page.html",
]

def convert(filename):
    path = os.path.join(TEMPLATES_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # فقط محتوای بین <main ...> و </main> رو نگه دار
    match = re.search(r'<main class="main">(.*?)</main>', content, re.DOTALL)
    if not match:
        print(f"⚠️  <main> پیدا نشد تو {filename}, این فایل دستی چک کن")
        return

    main_content = match.group(1)

    # مسیرهای assets/... رو به {% static 'assets/...' %} تبدیل کن
    main_content = re.sub(
        r'(src|href)="assets/([^"]+)"',
        r'\1="{% static \'assets/\2\' %}"',
        main_content,
    )

    page_name = filename.replace(".html", "").replace("-", "_")
    title = page_name.replace("_", " ").title()

    new_content = (
        "{% extends 'base.html' %}\n"
        "{% load static %}\n"
        f"{{% block title %}}{title}{{% endblock %}}\n"
        "{% block content %}\n"
        "<main class=\"main\">\n"
        f"{main_content}"
        "</main>\n"
        "{% endblock %}\n"
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"✅ {filename} تبدیل شد")


if __name__ == "__main__":
    for page in PAGES:
        convert(page)
        