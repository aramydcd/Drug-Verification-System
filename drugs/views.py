from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Drug
from .forms import DrugForm
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings


# Create your views here.
@login_required
def add_drug(request):
    # Only allow Admin or Company to add drugs
    if request.user.role not in ["Admin", "company"]:
        raise PermissionDenied("You are not allowed to add drugs.")

    if request.method == "POST":
        form = DrugForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            drug = form.save(commit=False)

            # Assign company if user is a company
            if request.user.role == "company":
                drug.company = request.user

            # If Admin is adding, let them choose company from form
            # (or optionally, Admin can skip assigning)
            drug.save()
            return redirect("view_drugs")
        else:
            print(form.errors)  # For debugging in terminal
    else:
        form = DrugForm(user=request.user)

    return render(request, "drugs/add_drug.html", {"form": form})


@login_required
def view_drugs(request):
    query = request.GET.get("q", "")

    # 🔎 Base queryset depending on user role
    if request.user.role == "Admin":
        drugs = Drug.objects.all()
    elif request.user.role == "company":
        drugs = Drug.objects.filter(company=request.user)
    else:
        drugs = Drug.objects.none()  # normal users shouldn't see drugs

    # 🔎 Search filter
    if query:
        drugs = drugs.filter(
            Q(name__icontains=query) | Q(batch_number__icontains=query)
        )

    return render(request, "drugs/view_drugs.html", {"drugs": drugs})


@login_required
def edit_drug(request, id):
    drug = get_object_or_404(Drug, id=id)
    old_image = drug.image.path if drug.image else None  # store old image path

    if request.method == "POST":
        form = DrugForm(request.POST, request.FILES, instance=drug, user=request.user)
        if form.is_valid():
            # If a new image is uploaded, delete the old one
            if 'image' in request.FILES and old_image and os.path.exists(old_image):
                os.remove(old_image)

            # Save the form
            form.save()
            return redirect("view_drugs")
    else:
        form = DrugForm(instance=drug, user=request.user)

    return render(request, "drugs/edit_drug.html", {"form": form, "drug": drug})


@login_required
def delete_drug(request, id):
    drug = get_object_or_404(Drug, id=id)
    drug.delete()
    return redirect("view_drugs")