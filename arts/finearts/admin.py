from django.contrib import admin
from .models import Student, Staff,StudentEvent
# Register your models here.

admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(StudentEvent)


#class StudentAdmin(admin.ModelAdmin):
 #   list_display = ('name', 'admission_number','department')
  #  search_fields = ('name', 'admission_number','department')