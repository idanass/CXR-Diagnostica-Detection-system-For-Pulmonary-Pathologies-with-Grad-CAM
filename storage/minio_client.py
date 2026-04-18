import os
import io
from datetime import datetime
from minio import Minio
from minio.error import S3Error

ENDPOINT   = os.getenv("MINIO_ENDPOINT",   "localhost:9000")
ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")

BUCKET_XRAYS   = "xrays"
BUCKET_REPORTS = "reports"


def get_client() -> Minio:
    return Minio(
        ENDPOINT,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=False
    )


def ensure_buckets():
    client = get_client()
    for bucket in [BUCKET_XRAYS, BUCKET_REPORTS]:
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)
            print(f"✅ Created bucket: {bucket}")


def upload_xray(image_bytes: bytes, filename: str) -> str:
    """Upload X-ray image → returns object name"""
    client = get_client()
    ensure_buckets()

    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"{ts}_{filename}"

    client.put_object(
        BUCKET_XRAYS, name,
        io.BytesIO(image_bytes), len(image_bytes),
        content_type="image/png"
    )
    return name


def upload_report(pdf_bytes: bytes, patient_name: str) -> str:
    """Upload PDF report → returns object name"""
    client = get_client()
    ensure_buckets()

    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"{ts}_{patient_name.replace(' ', '_')}_report.pdf"

    client.put_object(
        BUCKET_REPORTS, name,
        io.BytesIO(pdf_bytes), len(pdf_bytes),
        content_type="application/pdf"
    )
    return name