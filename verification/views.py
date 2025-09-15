from django.shortcuts import render, redirect
from .models import Verification
from drugs.models import Drug
from PIL import Image
import cv2
import numpy as np


def search_by_qr_code(request):
    result = None
    drug = None  

    if request.method == "POST":
        # case 1: manual input
        query = request.POST.get("qr_code", "").strip()  

        # case 2: uploaded image
        uploaded_file = request.FILES.get("qr_image")

        if uploaded_file:
            try:
                # Convert InMemoryUploadedFile to numpy array for cv2
                pil_image = Image.open(uploaded_file).convert("RGB")
                open_cv_image = np.array(pil_image)
                open_cv_image = open_cv_image[:, :, ::-1].copy()  # RGB → BGR

                # Use OpenCV QRCode detector
                detector = cv2.QRCodeDetector()
                data, vertices, _ = detector.detectAndDecode(open_cv_image)

                if data:
                    query = data  # QR code text
            except Exception as e:
                result = f"❌ Error decoding QR: {e}"

        if query:
            try:
                drug = Drug.objects.get(qr_code__iexact=query)  
                result = "Authentic ✅"
                is_valid = True
            except Drug.DoesNotExist:
                result = "Fake ❌"
                is_valid = False
                drug = None

            # save verification if user is logged in
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

