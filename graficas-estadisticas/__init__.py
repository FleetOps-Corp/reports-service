"""Entry point for Gráficas y Estadísticas microservice"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.presentation.main import app

if __name__ == "__main__":
    import uvicorn
    from src.infrastructure.config import get_settings
    
    settings = get_settings()
    
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        log_level=settings.LOG_LEVEL.lower(),
    )
