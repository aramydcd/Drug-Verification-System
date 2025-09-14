from django.shortcuts import render
from .models import Verification
from drugs.models import Drug

def home_view(request):
    recent_verifications = Verification.objects.select_related("drug", "user").order_by("-created_at")[:5]
    return render(request, 'home.html', {'recent_verifications': recent_verifications})


def search_by_batch(request):
    result = None
    drug = None  

    if request.method == "POST":
        query = request.POST.get("batch_number", "").strip()  # from form input name
        if query:
            try:
                # ✅ use batch_number instead of batch_number
                drug = Drug.objects.get(batch_number__iexact=query)  
                result = "Authentic ✅"
                is_valid = True
            except Drug.DoesNotExist:
                result = "Fake ❌"
                is_valid = False
                drug = None

            # ✅ Only save verification if we actually searched and we are logged in
            if request.user.is_authenticated:
                Verification.objects.create(
                    drug=drug,
                    user=request.user,
                    is_valid=is_valid
                )

    return render(
        request,
        "verification/search_by_batch.html",
        {"result": result, "drug": drug}
    )


def search_by_qr_code(request):
    result = None
    drug = None  

    if request.method == "POST":
        query = request.POST.get("qr_code", "").strip()  # from form input name
        if query:
            try:
                # ✅ use batch_number instead of batch_number
                drug = Drug.objects.get(qr_code__iexact=query)  
                result = "Authentic ✅"
                is_valid = True
            except Drug.DoesNotExist:
                result = "Fake ❌"
                is_valid = False
                drug = None

            # ✅ Only save verification if we actually searched and we are logged in
            if request.user.is_authenticated:
                Verification.objects.create(
                    drug=drug,
                    user=request.user,
                    is_valid=is_valid
                )

    return render(
        request,
        "verification/search_by_qr_code.html",
        {"result": result, "drug": drug}
    )

