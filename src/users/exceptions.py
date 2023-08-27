from fastapi import HTTPException, status


email_conflict_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Email already exists!"
)

username_conflict_exception = email_conflict_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Username already exists!"
)
