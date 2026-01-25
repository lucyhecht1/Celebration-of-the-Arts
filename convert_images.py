from PIL import Image
import os
import re  # For regex filename matching

# Define directories for Gallery 2024
input_folder = "static/images/gallery2024/"
output_folder = "static/images/gallery2024_compressed/"
skip_indices = [40, 67, 68, 69, 147]  # Missing images

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Regex pattern to match filenames like "image123.JPG"
filename_pattern = re.compile(r"image(\d+)\.(jpg|jpeg|png)$", re.IGNORECASE)

for filename in os.listdir(input_folder):
    # Check if filename matches expected pattern
    match = filename_pattern.match(filename)
    if not match:
        print(f"⚠️ Skipping unexpected file format: {filename}")
        continue  # Skip non-matching files

    file_index = int(match.group(1))  # Extract the number from filename

    # Skip missing images
    if file_index in skip_indices:
        print(f"🚫 Skipping missing image: {filename}")
        continue  

    # Open image
    img_path = os.path.join(input_folder, filename)
    img = Image.open(img_path)

    # Generate WebP filename
    webp_filename = os.path.splitext(filename)[0] + ".webp"
    output_path = os.path.join(output_folder, webp_filename)

    # Skip if already converted
    if os.path.exists(output_path):
        print(f"✅ Skipping (already converted): {filename}")
        continue

    # Resize images (optional, max width 1200px)
    max_width = 1200
    if img.width > max_width:
        new_height = int((max_width / img.width) * img.height)
        img = img.resize((max_width, new_height), Image.LANCZOS)

    # Save as WebP
    img.save(output_path, "WEBP", quality=85)

    print(f"✅ Converted & Compressed: {filename} → {webp_filename}")

print("🎉 Gallery 2024 images have been converted to WebP and compressed!")
