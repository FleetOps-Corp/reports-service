"""Application Layer - Service Aggregators
Responsabilidad: Agregar datos de servicios externos
Patrón: Aggregator Pattern
Capa: Application
"""
from typing import Dict, List, Optional
from ...infrastructure.grpc_clients import (
    VehicleServiceClient,
    AssignmentServiceClient,
    IncidentServiceClient,
    MaintenanceServiceClient,
)


class ExternalServiceAggregator:
    """Agrega datos de múltiples servicios externos."""
    
    def __init__(
        self,
        vehicle_client: VehicleServiceClient,
        assignment_client: AssignmentServiceClient,
        incident_client: IncidentServiceClient,
        maintenance_client: MaintenanceServiceClient,
    ):
        self.vehicle_client = vehicle_client
        self.assignment_client = assignment_client
        self.incident_client = incident_client
        self.maintenance_client = maintenance_client
    
    async def aggregate_fleet_data(self, location: str) -> Dict:
        """Aggregate all fleet data from external services."""
        try:
            incidents = await self.incident_client.get_incidents(location)
            maintenances = await self.maintenance_client.get_maintenance_records(location)
            
            return {
                "incidents": incidents,
                "maintenances": maintenances,
            }
        except Exception as e:
            raise RuntimeError(f"Failed to aggregate fleet data: {e}")
