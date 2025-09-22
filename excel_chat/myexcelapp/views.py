import pandas as pd
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os, json


CURRENT_FILE_PATH = "uploaded_file.xlsx"

@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            return JsonResponse({"error": "No file provided"}, status=400)

        if not uploaded_file.name.endswith((".xls", ".xlsx")):
            return JsonResponse({"error": "Invalid file format"}, status=400)

        path = default_storage.save(CURRENT_FILE_PATH, ContentFile(uploaded_file.read()))
        df = pd.read_excel(path)

        return JsonResponse({"columns": list(df.columns)})
    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def perform_operation(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            operation = data.get("operation")
            params = data.get("params")

            if not os.path.exists(CURRENT_FILE_PATH):
                return JsonResponse({"error": "No file uploaded"}, status=400)

            df = pd.read_excel(CURRENT_FILE_PATH)

            if operation == "add_column":
                new_col = params.get("new_column_name")
                if not new_col:
                    return JsonResponse({"error": "Missing new_column_name"}, status=400)
                df[new_col] = None  

            elif operation == "sum":
                new_col = params.get("new_column_name")
                cols = params.get("columns_to_sum", [])
                if not new_col:
                    return JsonResponse({"error": "New column not created"}, status=400)
                col_list=df.columns
                for i in cols:
                    if i not in col_list:
                        return JsonResponse({"error": "Column not found"}, status=400)        
                df[new_col] = df[cols[0]] + df[cols[1]]

            else:
                return JsonResponse({"error": "Invalid operation"}, status=400)

            df.to_excel(CURRENT_FILE_PATH, index=False)

            return JsonResponse({
                "columns": list(df.columns),
                "preview": df.head().to_dict(orient="records")
            })
        except Exception as e:
            return JsonResponse({"operation error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)


def download_file(request):
    if not os.path.exists(CURRENT_FILE_PATH):
        return JsonResponse({"error": "No file available"}, status=400)
    response = FileResponse(open(CURRENT_FILE_PATH, "rb"), as_attachment=True, filename="result.xlsx")
    return response
