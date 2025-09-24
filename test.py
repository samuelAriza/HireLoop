import os
import requests
import uuid

OUTPUT_DIR = "media/projects/dummy"
NUM_IMAGES = 20
WIDTH, HEIGHT = 800, 600

def download_picsum_images():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i in range(1, NUM_IMAGES + 1):
        seed = uuid.uuid4().hex
        url = f"https://picsum.photos/seed/{seed}/{WIDTH}/{HEIGHT}"
        filename = os.path.join(OUTPUT_DIR, f"dummy{i}.jpg")

        print(f"Descargando {url} -> {filename}")
        response = requests.get(url)

        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
        else:
            print(f"❌ Error al descargar {url} (status {response.status_code})")

    print(f"\n✅ Descargadas {NUM_IMAGES} imágenes en {OUTPUT_DIR}")

if __name__ == "__main__":
    download_picsum_images()
