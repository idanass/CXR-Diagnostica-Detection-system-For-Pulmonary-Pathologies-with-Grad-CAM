import mlflow
import os
from datetime import datetime

MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")

def setup_mlflow():
    mlflow.set_tracking_uri(MLFLOW_URI)
    mlflow.set_experiment("CXR-Diagnostica")
    print(f"✅ MLflow connected → {MLFLOW_URI}")


def log_prediction(
    filename:        str,
    predictions:     dict,   # { pathology: {score, cam_base64} }
    inference_time:  float,
    patient_id:      str = "anonymous",
):
    """
    Log one inference run to MLflow.
    """
    with mlflow.start_run(run_name=f"predict_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):

        # ── Tags ────────────────────────────────────
        mlflow.set_tags({
            "model":      "densenet121-res224-nih",
            "filename":   filename,
            "patient_id": patient_id,
            "source":     "api"
        })

        # ── Params ──────────────────────────────────
        mlflow.log_params({
            "model_weights": "densenet121-res224-nih",
            "image_size":    224,
            "pathologies":   14,
        })

        # ── Metrics ─────────────────────────────────
        mlflow.log_metric("inference_time_sec", inference_time)

        # Log each pathology score
        for name, data in predictions.items():
            safe_name = name.replace(" ", "_").replace("/", "_")
            mlflow.log_metric(f"score_{safe_name}", data["score"])

        # Top finding
        top = max(predictions.items(), key=lambda x: x[1]["score"])
        mlflow.log_metric("top_score", top[1]["score"])
        mlflow.set_tag("top_finding", top[0])

        print(f"📊 MLflow run logged — top: {top[0]} ({top[1]['score']:.4f})")