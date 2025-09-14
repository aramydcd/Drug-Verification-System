import os
import django
import qrcode

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drug_verification_system.settings")  # change to your project name
django.setup()

from drugs.models import Drug   # import your Drug model

def generate_qr_codes(output_folder="media/qr_test"):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    drugs = Drug.objects.all()
    for drug in drugs:
        qr_text = drug.qr_code   # or drug.qr_code_text if you have that field

        if not qr_text:
            print(f"Skipping {drug.name} (no QR text)")
            continue

        # Generate QR code
        img = qrcode.make(qr_text)

        # Save as <batch_number>.png
        filename = f"{drug.qr_code}.png"
        filepath = os.path.join(output_folder, filename)
        img.save(filepath)

        print(f"✅ Saved QR code for {drug.name} at {filepath}")

if __name__ == "__main__":
    generate_qr_codes()
