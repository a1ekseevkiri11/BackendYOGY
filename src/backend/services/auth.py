from datetime import timedelta, datetime

import bcrypt
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from fastapi import Depends, HTTPException, status
from jwt import PyJWTError
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend import tables
from backend.models import auth as models
from backend.settings import settings

import jwt
from jwt import PyJWTError

oauth_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
security = HTTPBearer()


class AuthServices:
    @classmethod
    def hash_password(cls, password: str):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    @classmethod
    def validate_password(cls, password: str, hash_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode(), hash_password)

    @classmethod
    def encode_jwt(
            cls,
            payload: dict,
            private_key: str = settings.private_key_path.read_text(),
            algorithm: str = settings.algorithm,
            expire_timedelta: timedelta | None = None,
            expire_minutes: int = settings.access_token_expire,
    ):

        to_encode = payload.copy()
        now = datetime.utcnow()

        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)

        to_encode.update(
            exp=expire,  # Время, когда токен закончит свою работу
            iat=now,  # Время, когда выпущен токен
        )

        return jwt.encode(to_encode, key=private_key, algorithm=algorithm)

    @classmethod
    def decode_jwt(
            cls,
            token: str | bytes,
            public_key: str = settings.public_key_path.read_text(),
            algorithms: str = settings.algorithm) -> dict:

        return jwt.decode(token, key=public_key, algorithms=[algorithms])

    async def validate_token(
            self,
            token,
    ) -> models.User:

        confirm_user = self.decode_jwt(token).get("user")

        try:
            user = models.User.parse_obj(confirm_user)
        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials") from None

        return user

    async def get_current_user(self, token: str = Depends(oauth_schema)) -> models.User:
        return await self.validate_token(token)

    def create_token(self, user: tables.User) -> models.Token:
        userdata = models.User(
            id=user.id,
            username=user.username
        )

        payload = {
            "sub": str(userdata.id),
            "user": userdata.dict()
        }

        return models.Token(access_token=self.encode_jwt(payload))

    async def login(self, username: str, password: str, session: AsyncSession) -> models.Token:
        stmt = select(tables.User).where(tables.User.username == username)
        db_response = await session.execute(stmt)
        user = db_response.scalar()

        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User does not exist, please register")

        # hashed_password = str.encode(user.password, encoding="utf-8")

        if self.validate_password(password, str.encode(user.password, encoding="utf-8")):
            return self.create_token(user)

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

    async def register(self, user_data: models.UserRegister, session: AsyncSession):
        stmt = select(tables.User).where(tables.User.username == user_data.username)
        db_response = await session.execute(stmt)
        db_user = db_response.scalar()
        print(1)
        if db_user is None:
            user = tables.User(
                username=user_data.username,
                password=str(self.hash_password(user_data.password))
            .replace("b'", "").replace("'", "")

            )
            print(2)
            session.add(user)
            await session.commit()

            return self.create_token(user)
        else:
            print(3)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Users already exist",
                headers={
                    "WWW-Authenticate": 'Bearer'
                }
            )


services = AuthServices()
