import json
import pandas as pd
from datetime import datetime
from config import OUTPUT_DIR


def generate_work_order(report_data: dict) -> dict:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    equipment_id = report_data.get("equipment_id", "UNKNOWN")

    filename_base = f"work_order_{equipment_id}_{timestamp}"
    excel_path = OUTPUT_DIR / f"{filename_base}.xlsx"
    json_path = OUTPUT_DIR / f"{filename_base}.json"

    with open(json_path, "w") as f:
        json.dump(report_data, f, indent=4)

    df = pd.DataFrame([
        {"Field": "Equipment ID", "Value": report_data.get("equipment_id", "")},
        {"Field": "Symptoms", "Value": report_data.get("symptoms", "")},
        {"Field": "Diagnosis", "Value": report_data.get("diagnosis", "")},
        {"Field": "Severity", "Value": report_data.get("severity", "")},
        {"Field": "Action Plan", "Value": report_data.get("action_plan", "")},
        {"Field": "Parts Required", "Value": report_data.get("parts_required", "")},
        {"Field": "Estimated Hours", "Value": report_data.get("estimated_hours", "")},
        {"Field": "Confidence Score", "Value": report_data.get("confidence_score", "")},
    ])

    df.to_excel(excel_path, index=False)

    return {
        "excel_path": str(excel_path),
        "json_path": str(json_path),
        "status": "success"
    }