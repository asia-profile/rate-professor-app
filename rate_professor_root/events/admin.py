from django.contrib import admin
from .models import Student, Module, Professor, Rating

# Register your models here.
admin.site.register(Student)
admin.site.register(Module)
admin.site.register(Professor)
admin.site.register(Rating)
