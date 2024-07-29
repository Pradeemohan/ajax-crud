# views.py

from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Employee
from .forms import EmployeeForm

def index(request):
    return render(request, 'employees/index.html')

def get_employees(request):
    employees = Employee.objects.all().values('id', 'name', 'email', 'password')
    return JsonResponse(list(employees), safe=False)

@csrf_exempt
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:index')  # Redirect to your employee list page (replace 'index' with your actual URL name)
        else:
            return JsonResponse(form.errors, status=400)
    else:
        form = EmployeeForm()
    return render(request, 'employees/add.html', {'form': form})

@csrf_exempt
def update_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('myapp:index')  # Redirect to index page after successful edit
        else:
            return JsonResponse(form.errors, status=400)
    
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/edit.html', {'form': form, 'employee': employee})

@csrf_exempt
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        employee.delete()
        return JsonResponse({'message': 'Employee deleted successfully.'})
    else:
        return JsonResponse({'error': 'POST method required.'}, status=405)

def get_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    data = {
        'id': employee.id,
        'name': employee.name,
        'email': employee.email,
        'password': employee.password
    }
    return JsonResponse(data)
