#from passlib.context import CryptContext
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#pwd_context.hash("password")

users_db = {
    "kit": {
        "username": "kit",
        "hashed_password": "$2b$12$ZYxkM7M7n9O5VChXQJ14C.fsaJF3teC1s/nVvH2Zgtr.jC3arT6nW",
        "level": 3
    },
    "dtu": {
        "username": "dtu",
        "hashed_password": "$2b$12$5c1w2iD9QzbScK1H2IpM.OzzOxKMCkdw1MN40bfBk8pIt1RV0ZA4C",
        "level": 3
    },
    "3ds": {
        "username": "3ds",
        "hashed_password": "$2b$12$6zTaSVvVBkOWPX5Br8ockOPC327ZO1vLMcgmYS4FQEb9d6nJ.VqO.",
        "level": 3
    },
    "other": {
        "username": "other",
        "hashed_password": "$2b$12$pVLGI9niLwycwIkUr8usH.kA6jgQlMRrBTG66cR7rciTWHS1T0Vqm",
        "level": 3
    }
}