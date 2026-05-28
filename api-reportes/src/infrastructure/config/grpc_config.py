"""Infrastructure Layer - gRPC Configuration
Responsabilidad: Configuración de canales gRPC
Capa: Infrastructure
"""
from typing import Optional
import grpc
import logging

logger = logging.getLogger(__name__)


class GRPCConfig:
    """Configuración para conexiones gRPC."""
    
    def __init__(self, settings):
        self.settings = settings
        self.channels: dict = {}
    
    async def get_channel(self, service_name: str) -> grpc.aio.Channel:
        """Get or create gRPC channel for service."""
        if service_name not in self.channels:
            target = f"{service_name}:{self.settings.GRPC_PORT}"
            self.channels[service_name] = grpc.aio.secure_channel(target)
            logger.info(f"Created gRPC channel to {target}")
        
        return self.channels[service_name]
    
    async def close_channels(self):
        """Close all gRPC channels."""
        for service_name, channel in self.channels.items():
            try:
                await channel.close()
                logger.info(f"Closed gRPC channel: {service_name}")
            except Exception as e:
                logger.error(f"Error closing channel {service_name}: {e}")
