from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Drug
from .forms import DrugForm

# Create your views here.
def is_admin(user):
    return user.is_authenticated and user.role == 'Admin'

@user_passes_test(is_admin)
def add_drug(request):
    
    if request.method == 'POST':
        form = DrugForm(request.POST, request.FILES)
        if form.is_valid():
            drug = form.save(commit=False)
            drug.company = request.user   # 🔑 Assign current company
            drug.save()
            return redirect('view_drugs')
    else:
        form = DrugForm()
    return render(request, 'drugs/add_drug.html', {'form': form})


@user_passes_test(is_admin)
def view_drugs(request):
    drugs = Drug.objects.all()
    return render(request, 'drugs/view_drugs.html', {'drugs': drugs})

@user_passes_test(is_admin)
def edit_drug(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id, company=request.user)  # 🔒 ensure ownership    
    if request.method == 'POST':
        form = DrugForm(request.POST, request.FILES, instance=drug)
        if form.is_valid():
            form.save()
            return redirect('view_drugs')
    else:
        form = DrugForm(instance=drug)
    return render(request, 'drugs/edit_drug.html', {'form': form})

@user_passes_test(is_admin)
def delete_drug(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id, company=request.user)  # 🔒 ensure ownership
    if request.method == "POST":
        drug.delete()
        return redirect("view_drugs")
    return render(request, "drugs/delete_drug.html", {"drug": drug})
