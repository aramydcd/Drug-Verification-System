from django.shortcuts import render
from .models import Verification, Drug

def home(request):
    recent_verifications = Verification.objects.select_related("drug", "user").order_by("-created_at")[:5]
    return render(request, 'home.html', {'recent_verifications': recent_verifications})


def search_by_batch(request):
    query = request.GET.get("batch_code")
    result = None
    if query:
        try:
            drug = Drug.objects.get(batch_code=query)
            result = "Authentic ✅"
            is_valid = True
        except Drug.DoesNotExist:
            drug = None
            result = "Fake ❌"
            is_valid = False

        # Save verification history
        Verification.objects.create(
            drug=drug if drug else None,
            user=request.user if request.user.is_authenticated else None,
            is_valid=is_valid
        )

    return render(request, "verification/search_by_batch.html", {"result": result})
