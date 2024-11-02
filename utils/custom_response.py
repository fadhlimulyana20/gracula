# utils.py
import time
from rest_framework.response import Response
from rest_framework import status

def custom_response(
    data=None, 
    message="success", 
    code=status.HTTP_200_OK, 
    meta=None, 
    errors=None
):
    start_time = time.time()  # Record the start time for process time calculation

    # Calculate processing time in milliseconds
    process_time = int((time.time() - start_time) * 1000)

    response_data = {
        "message": message,
        "code": code,
        "data": data,
        "meta": meta or {},  # Default to empty dict if no meta is provided
        "process_time": process_time,
        "errors": errors,
    }
    # Remove keys with None values (optional)
    response_data = {k: v for k, v in response_data.items() if v is not None}
    
    return Response(response_data, status=code)
