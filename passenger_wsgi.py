from chat_app.wsgi import application

#import sys
#import os

# 🔴 هام جداً: غيّر هذا المسار إلى المسار الصحيح لمشروعك
# المسار يكون عادة: /home/اسم_المستخدم/اسم_مجلد_المشروع
# مثال: /home/englishlearn/chat_app_project
#PROJECT_PATH = '/home/deepoaji/EnglishLearn'  # غيّر هذا!

# أضف مسار المشروع إلى sys.path
#if PROJECT_PATH not in sys.path:
#    sys.path.insert(0, PROJECT_PATH)

# عيّن متغير إعدادات Django
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

# استدعاء تطبيق Django
#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()
