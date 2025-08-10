from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from typing import Optional

from database.connection import get_db
from models.usuario import Usuario, UsuarioCreate, UsuarioLogin

SECRET_KEY = "tu_clave_secreta_aqui"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

class AuthService:
    def authenticate_user(self, db: Session, username: str, password: str) -> str:
        """Autenticar usuario y retornar token JWT"""
        # Simulación de autenticación - en producción usar hash de contraseñas
        if username == "agapitomiralles123" and password == "password":
            token = self.create_access_token(data={"sub": username})
            return token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    def create_access_token(self, data: dict) -> str:
        """Crear token JWT"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[str]:
        """Verificar token JWT"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return None
            return username
        except jwt.PyJWTError:
            return None

    def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> Usuario:
        """Obtener usuario actual desde token"""
        token = credentials.credentials
        username = self.verify_token(token)
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        # Simulación de usuario - en producción buscar en base de datos
        user = Usuario(
            id=1,
            username=username,
            email="admin@chango-adm.com",
            nombre_completo="Administrador",
            fecha_creacion=datetime.utcnow(),
            activo=True
        )
        return user

    def create_user(self, db: Session, user: UsuarioCreate) -> Usuario:
        """Crear nuevo usuario"""
        # Simulación de creación de usuario
        new_user = Usuario(
            id=2,
            username=user.username,
            email=user.email,
            nombre_completo=user.nombre_completo,
            fecha_creacion=datetime.utcnow(),
            activo=True
        )
        return new_user
