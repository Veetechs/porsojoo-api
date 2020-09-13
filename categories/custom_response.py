def custom_response(message, data, description=None, is_success=True):
    response = {
        "message": message,
        "data": data,
        "is_success": is_success,
        "description": description
    }
    return response
