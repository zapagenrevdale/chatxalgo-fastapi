from fastapi import HTTPException, status


credential_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password"
)

unauthorize_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)


token_credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

inactive_user_exception = HTTPException(status_code=400, detail="Inactive user")
