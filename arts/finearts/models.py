from django.db import models


# Event model with category field to distinguish between onstage and offstage events
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('onstage', 'On-stage'),
        ('offstage', 'Off-stage'),
    ]
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='offstage')
    accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


# Student model with Many-to-Many relationship to Event model through StudentEvent model
class Student(models.Model):
    name = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=15, unique=True)
    department = models.CharField(max_length=50)
    events = models.ManyToManyField(Event, through='StudentEvent')
    

    def __str__(self):
        return self.name


# Staff model
class Staff(models.Model):
    name = models.CharField(max_length=100)
    sid = models.CharField(max_length=15, unique=True, default='')
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class StudentEvent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    admission_number = models.CharField(max_length=20, blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    result = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        unique_together = ('student', 'event')

    def __str__(self):
        return f"{self.student.name} - {self.event.name}"



class HomePageContent(models.Model):
    title = models.CharField(max_length=100, default="Welcome to St.Thomas")
    faculty_login_url = models.URLField(max_length=200, default="#")
    student_login_url = models.URLField(max_length=200, default="#")
    parent_login_url = models.URLField(max_length=200, default="#")
    footer_text = models.CharField(max_length=200, default="Powered by Linways Technologies Pvt. Ltd.")
    logo_image = models.ImageField(upload_to='logos/', blank=True, null=True)  # Upload logo dynamically

    def __str__(self):
        return self.title

