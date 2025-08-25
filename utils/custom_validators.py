from fastapi import HTTPException

def validate_api_key(api_key):
    if api_key!="XXXX":
        raise HTTPException(status_code=404, detail="Invalid API Key")
