from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Event ,Staff ,StudentEvent

# Register View
def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        admission_number = request.POST.get('admission_number')
        department = request.POST.get('department')

        # Check if admission number is unique
        if Student.objects.filter(admission_number=admission_number).exists():
            messages.error(request, 'Admission number already exists.')
            return render(request, 'register.html')

        # Create a new student
        Student.objects.create(name=name, admission_number=admission_number, department=department)
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')

    return render(request, 'register.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username and password match an existing admission number
        if Student.objects.filter(admission_number=username).exists() and username == password:
            request.session['user'] = username
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')

# Dashboard View
def dashboard_view(request):
    """
    Dashboard view that handles user profile and event registration.
    """
    # Check if user is logged in
    user = request.session.get('user', None)
    if not user:
        messages.error(request, 'Please log in first.')
        return redirect('login')

    # Fetch the student's details
    try:
        student = Student.objects.get(admission_number=user)
    except Student.DoesNotExist:
        messages.error(request, 'Invalid session. Please log in again.')
        return redirect('login')

    # Event registration logic
    if request.method == 'POST':
        # Retrieve selected offstage, onstage, and group events from the form
        selected_offstage_events = request.POST.getlist('offstage_events[]')
        selected_onstage_events = request.POST.getlist('onstage_events[]')
        selected_group_events = request.POST.getlist('group_events[]')

        # Combine group events with onstage events
        selected_onstage_events.extend(selected_group_events)  # Add group events to onstage events

        # Limit registration to a maximum of 3 offstage events and 3 onstage events (including group events)
        if len(selected_offstage_events) > 3:
            messages.error(request, 'You can only register for a maximum of 3 offstage events.')
        elif len(selected_onstage_events) > 3:
            messages.error(request, 'You can only register for a maximum of 3 onstage events.')
        elif len(selected_offstage_events) + len(selected_onstage_events) > 6:
            messages.error(request, 'You can only register for a total of 6 events (3 offstage and 3 onstage).')
        else:
            # Clear existing events before adding new ones
            student.events.clear()

            # Register the selected offstage events
            for event_name in selected_offstage_events:
                event, _ = Event.objects.get_or_create(name=event_name, category='offstage')
                student.events.add(event)

            # Register the selected onstage events (including group events)
            for event_name in selected_onstage_events:
                event, _ = Event.objects.get_or_create(name=event_name, category='onstage')
                student.events.add(event)

            messages.success(request, 'You have successfully registered for the selected events.')
            return redirect('user_profile')  # Redirect to the user profile page

    # Fetch all available events (onstage and offstage)
    offstage_events = Event.objects.filter(category='offstage')
    onstage_events = Event.objects.filter(category='onstage')

    # Fetch registered events
    registered_events = student.events.all()

    # Render the dashboard template with necessary context
    return render(request, 'dashboard.html', {
        'student': student,
        'registered_events': registered_events,
        'offstage_events': offstage_events,
        'onstage_events': onstage_events,
    })

# User Profile View
def user_profile_view(request):
    """
    View to display the user's profile, including name, department, and selected events.
    """
    user = request.session.get('user', None)
    if not user:
        messages.error(request, 'Please log in first.')
        return redirect('login')

    try:
        student = Student.objects.get(admission_number=user)
    except Student.DoesNotExist:
        messages.error(request, 'Invalid session. Please log in again.')
        return redirect('login')

    # Fetch registered events
    registered_events = student.events.all()

    return render(request, 'user_profile.html', {
        'student': student,
        'registered_events': registered_events,
    })

    #admin_dashboard view
def admin_dashboard(request):
    # Fetch all students who have at least one accepted event
    students = Student.objects.prefetch_related('events').all()
    total_students = students.count()
    total_capacity = 3000  # Set your capacity

    # Data for accepted events only (Events explicitly accepted by teachers)
    accepted_student_data = []
    for student in students:
        student_accepted_events = [event.name for event in student.events.filter(studentevent__accepted=True)]
        if student_accepted_events:
            accepted_student_data.append({
                'name': student.name,
                'admission_number': student.admission_number,
                'department': student.department,
                'accepted_events': student_accepted_events,
            })

    # Unique departments
    departments = students.values_list('department', flat=True).distinct()

    # Unique accepted events
    accepted_events = Event.objects.filter(studentevent__accepted=True).values_list('name', flat=True).distinct()

    return render(request, 'admin_dashboard.html', {
        'total_students': total_students,
        'total_capacity': total_capacity,
        'accepted_students': accepted_student_data,  # Only accepted events
        'departments': departments,  # For department filter
        'events': accepted_events,  # Only accepted events
    })



def staff_register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        sid = request.POST.get('sid')
        department = request.POST.get('department')

        # Check if admission number is unique
        if Staff.objects.filter(sid=sid).exists():
            messages.error(request, ' id already exists.')
            return render(request, 'staff_register.html')

        # Create a new student
        Staff.objects.create(name=name, sid=sid, department=department)
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('staff_login')

    return render(request, 'staff_register.html')



def staff_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username and password match an existing admission number
        if Staff.objects.filter(sid=username).exists() and username == password:
            request.session['user'] = username
            return redirect('teachers')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'staff_login.html')

    return render(request, 'staff_login.html')


#teachers view

def teachers_view(request):
    """
    View to display students in the teacher's department along with their registered events.
    """
    # Check if the teacher is logged in
    user = request.session.get('user', None)
    if not user:
        messages.error(request, 'Please log in first.')
        return redirect('staff_login')

    try:
        # Get the logged-in teacher's details
        teacher = Staff.objects.get(sid=user)
    except Staff.DoesNotExist:
        messages.error(request, 'Invalid session. Please log in again.')
        return redirect('staff_login')

    # Filter students by the teacher's department
    students = Student.objects.filter(department=teacher.department).prefetch_related('events')

    # Prepare data for the template
    student_event_data = []
    for student in students:
        events = []
        for event in student.events.all():
            student_event = StudentEvent.objects.filter(student=student, event=event).first()
            events.append({
                'event': event,
                'accepted': student_event.accepted if student_event else False
            })
        student_event_data.append({
            'student': student,
            'events': events
        })

    return render(request, 'teachers.html', {
        'teacher_department': teacher.department,
        'students': student_event_data,
    })


def accept_event(request):
    """
    View to handle event acceptance by a teacher for a specific student-event pair.
    """
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        student_id = request.POST.get('student_id')

        try:
            # Fetch the student-event relationship
            student_event = StudentEvent.objects.get(student_id=student_id, event_id=event_id)

            # Mark the event as accepted for this specific student
            student_event.accepted = True
            student_event.save()

            messages.success(request, f"Event '{student_event.event.name}' accepted for {student_event.student.name}.")
        except StudentEvent.DoesNotExist:
            messages.error(request, "Invalid student or event, or the student is not registered for this event.")

    return redirect('teachers')


#home

def home(request):
    return render(request, 'home.html') 



#ulpoad results
def upload_results(request):
    selected_event_id = request.GET.get("event", None)  # Filter by event if selected
    events = Event.objects.filter(studentevent__accepted=True).distinct()

    student_events = StudentEvent.objects.filter(accepted=True).select_related('student', 'event')
    if selected_event_id:
        student_events = student_events.filter(event_id=selected_event_id)

    return render(request, "upload_results.html", {
        "events": events,
        "student_events": student_events
    })



def submit_results(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("result_"):
                _, student_id, event_id = key.split("_")
                try:
                    student_event = StudentEvent.objects.get(student_id=student_id, event_id=event_id)
                    student_event.result = value
                    student_event.save()
                except StudentEvent.DoesNotExist:
                    messages.error(request, f"Error saving result for Student ID {student_id}, Event ID {event_id}")

        messages.success(request, "Results uploaded successfully!")
        return redirect("upload_results")

    return redirect("admin_dashboard")


def student_dashboard(request): 
    student = None  
    accepted_events = []  
    
    if hasattr(request.user, 'student'):  # Ensure user is a student
        student = request.user.student
        accepted_events = StudentEvent.objects.filter(student=student, accepted=True).select_related('event')

    print("Student:", student)  # Debugging print statement
    print("Accepted Events:", accepted_events)  # Debugging print statement

    return render(request, 'student_dashboard.html', {
        'student': student,  
        'accepted_events': accepted_events,  
    })



