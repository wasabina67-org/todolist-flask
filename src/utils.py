def status_success():
    return {"status": "success"}


def status_error(ex):
    return {"status": "error", "message": str(ex)}
