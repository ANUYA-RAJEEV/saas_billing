from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Company
from .forms import LoginForm, CompanyForm, RegisterCompanyForm

def login_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'userprofile'):
            if request.user.userprofile.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif request.user.userprofile.role == 'COMPANY':
                return redirect('company_dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(request, username=u, password=p)
            if user is not None:
                login(request, user)
                if hasattr(user, 'userprofile'):
                    if user.userprofile.role == 'ADMIN':
                        return redirect('admin_dashboard')
                    elif user.userprofile.role == 'COMPANY':
                        return redirect('company_dashboard')
            # Add error message if user not found or auth fails
            form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'billing_portal/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def admin_dashboard(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'ADMIN':
        return redirect('login')
    companies = Company.objects.all()
    return render(request, 'billing_portal/admin_dashboard.html', {'companies': companies})

@login_required
def register_company(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'ADMIN':
        return redirect('login')
    
    if request.method == 'POST':
        form = RegisterCompanyForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            cname = form.cleaned_data['company_name']
            
            if not User.objects.filter(username=u).exists():
                user = User.objects.create_user(username=u, password=p)
                UserProfile.objects.create(user=user, role='COMPANY')
                Company.objects.create(user=user, company_name=cname)
                return redirect('admin_dashboard')
            else:
                form.add_error('username', 'Username already exists')
    else:
        form = RegisterCompanyForm()
    
    return render(request, 'billing_portal/register_company.html', {'form': form})

@login_required
def edit_company(request, pk):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'ADMIN':
        return redirect('login')
    company = get_object_or_404(Company, pk=pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = CompanyForm(instance=company)
    return render(request, 'billing_portal/edit_company.html', {'form': form, 'company': company})

@login_required
def delete_company(request, pk):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'ADMIN':
        return redirect('login')
    company = get_object_or_404(Company, pk=pk)
    user = company.user
    if request.method == 'POST':
        user.delete() # Unlinks and deletes the company and profile automatically via cascade
        return redirect('admin_dashboard')
    return render(request, 'billing_portal/delete_company.html', {'company': company})

@login_required
def company_dashboard(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'COMPANY':
        return redirect('login')
    company = get_object_or_404(Company, user=request.user)
    return render(request, 'billing_portal/company_dashboard.html', {'company': company})

@login_required
def billing_view(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'COMPANY':
        return redirect('login')
    company = get_object_or_404(Company, user=request.user)
    return render(request, 'billing_portal/billing_page.html', {'company': company})
