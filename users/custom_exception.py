def exception(message, is_success, data=None, description=None):
    exception_data = {
        "message": message,
        "is_success": is_success,
        "data":data,
        "description": description
    }
    return exception_data

