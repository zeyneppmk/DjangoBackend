import cloudinary.uploader
import cloudinary.exceptions
import httpx
import os
import aiofiles


def upload_to_cloudinary(file_path, folder="transcripts"):
    try:
        upload_result = cloudinary.uploader.upload(
            file_path,
            resource_type="raw",  # raw = ses, txt, pdf gibi dosyalar için
            folder=folder
        )
        return upload_result["secure_url"]
    except cloudinary.exceptions.Error as e:
        raise Exception(f"Cloudinary upload failed: {str(e)}")

async def send_audio_to_fastapi(file_path):
    # Doğru FastAPI endpoint
    fastapi_url = "http://fastapi:8000/transcribe/"

    try:
        timeout = httpx.Timeout(60.0)  # 60 saniye veriyoruz
        async with httpx.AsyncClient(timeout=timeout) as client:
            with open(file_path, "rb") as f:
                files = [("files", (os.path.basename(file_path), f, "audio/wav"))]
                response = await client.post(fastapi_url, files=files)

        # Hata varsa Exception fırlat
        response.raise_for_status()

        # Başarılı yanıtı JSON olarak döndür
        return response.json()

    except httpx.HTTPError as e:
        raise Exception(f"FastAPI iletişim hatası: {str(e)}")

