# -*- coding: utf-8 -*-
"""
Middleware para CORS (Cross-Origin Resource Sharing)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import CORS_ORIGINS

def setup_cors(app: FastAPI):
    """
    Configurar middleware CORS
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ) 