"""Application Layer - Use Cases
Responsabilidad: Orquestar lógica de dominio e infraestructura.
Patrón: Use Case / Application Service
Capa: Application
"""
from typing import List
from datetime import datetime
from ..dto import AvailabilityReportDTO, TraceabilityDTO, MaintenanceMetricsDTO
from ...domain.models import VehicleSnapshot, Incident, Maintenance
from ...domain.services import (
    AvailabilityCalculator,
    MTTRCalculator,
    MaintenanceAnalyzer,
    IncidentAggregator
)
from ...domain.repositories import (
    VehicleSnapshotRepository,
    IncidentRepository,
    MaintenanceRepository
)


class GetAvailabilityReportUseCase:
    """Use Case: Obtener reporte de disponibilidad de flota.
    
    Transactional Example: Orquesta el flujo completo
    Entrada: site_id → Salida: AvailabilityReportDTO
    
    Patrón: Use Case / Application Service
    """
    
    def __init__(
        self,
        vehicle_snapshot_repo: VehicleSnapshotRepository,
        incident_repo: IncidentRepository,
    ):
        self.vehicle_snapshot_repo = vehicle_snapshot_repo
        self.incident_repo = incident_repo
    
    async def execute(self, fleet_location: str) -> AvailabilityReportDTO:
        """Execute use case: calcular disponibilidad.
        
        Flujo:
        1. Obtener snapshots de vehículos de la ubicación
        2. Calcular disponibilidad con AvailabilityCalculator
        3. Persistir snapshot histórico
        4. Retornar DTO
        
        Args:
            fleet_location: Ubicación/sede a reportar
            
        Returns:
            AvailabilityReportDTO: Reporte de disponibilidad
        """
        # Step 1: Retrieve vehicle snapshots
        vehicles = await self.vehicle_snapshot_repo.find_by_location(fleet_location)
        
        if not vehicles:
            # Default response if no vehicles found
            return AvailabilityReportDTO(
                fleet_location=fleet_location,
                total_vehicles=0,
                available_vehicles=0,
                availability_percentage=0.0,
                is_healthy=False,
                alert_level="CRITICAL"
            )
        
        # Step 2: Calculate availability
        kpi = AvailabilityCalculator.calculate_availability(vehicles, fleet_location)
        
        # Step 3: Populate additional metrics
        all_incidents = await self.incident_repo.find_by_vehicle_id("", days_back=30)
        kpi.incident_count_month = IncidentAggregator.count_incidents_in_month(all_incidents)
        
        # Step 4: Build response DTO
        return AvailabilityReportDTO(
            fleet_location=kpi.fleet_location,
            total_vehicles=kpi.total_vehicles,
            available_vehicles=kpi.available_vehicles,
            availability_percentage=kpi.availability_percentage,
            is_healthy=kpi.is_healthy(),
            alert_level=kpi.alert_level()
        )


class GetMaintenanceMetricsUseCase:
    """Use Case: Obtener métricas de mantenimiento.
    
    Patrón: Use Case / Application Service
    """
    
    def __init__(
        self,
        incident_repo: IncidentRepository,
        maintenance_repo: MaintenanceRepository,
    ):
        self.incident_repo = incident_repo
        self.maintenance_repo = maintenance_repo
    
    async def execute(self, fleet_location: str) -> MaintenanceMetricsDTO:
        """Execute: calcular métricas de mantenimiento.
        
        Args:
            fleet_location: Ubicación a analizar
            
        Returns:
            MaintenanceMetricsDTO: Métricas calculadas
        """
        # Query all maintenance events
        # Note: En producción, sería filtrado por vehículos de la ubicación
        maintenances: List[Maintenance] = []
        incidents: List[Incident] = []
        
        # Calculate MTTR
        mttr = MTTRCalculator.calculate_mttr(incidents)
        
        # Calculate preventive ratio
        preventive_ratio = MaintenanceAnalyzer.calculate_preventive_ratio(maintenances)
        
        preventive_count = sum(1 for m in maintenances if m.is_preventive())
        corrective_count = sum(1 for m in maintenances if m.is_corrective())
        
        return MaintenanceMetricsDTO(
            average_mttr_hours=mttr,
            preventive_maintenance_ratio=preventive_ratio,
            total_maintenance_events=len(maintenances),
            preventive_count=preventive_count,
            corrective_count=corrective_count,
            period_days=30
        )


class GetRecurrentIncidentsUseCase:
    """Use Case: Detectar vehículos con incidentes recurrentes.
    
    Patrón: Use Case / Application Service
    """
    
    def __init__(self, incident_repo: IncidentRepository):
        self.incident_repo = incident_repo
    
    async def execute(self, days_back: int = 30) -> List[dict]:
        """Execute: obtener ranking de incidentes recurrentes.
        
        Args:
            days_back: Período a analizar
            
        Returns:
            List[dict]: Ranking ordenado por frecuencia
        """
        # Implementation would query incidents and aggregate by vehicle
        return []


class GetVehicleTraceabilityUseCase:
    """Use Case: Obtener trazabilidad 360° de un vehículo.
    
    Transactional Example: Flujo completo atravesando todas las capas
    
    Patrón: Use Case / Application Service
    """
    
    def __init__(
        self,
        vehicle_snapshot_repo: VehicleSnapshotRepository,
        incident_repo: IncidentRepository,
        maintenance_repo: MaintenanceRepository,
    ):
        self.vehicle_snapshot_repo = vehicle_snapshot_repo
        self.incident_repo = incident_repo
        self.maintenance_repo = maintenance_repo
    
    async def execute(self, vehicle_id: str) -> TraceabilityDTO:
        """Execute: compilar trazabilidad completa del vehículo.
        
        Flujo end-to-end:
        1. [Presentation] Recibir vehicle_id
        2. [Application] Coordinar repositorios
        3. [Domain] Modelos de dominio
        4. [Infrastructure] Consultar MongoDB
        5. [Domain] Calcular métricas
        6. [Application] Transformar a DTO
        7. [Presentation] Retornar JSON
        
        Args:
            vehicle_id: ID del vehículo
            
        Returns:
            TraceabilityDTO: Historial completo
        """
        # Step 1: Get latest snapshot (Infrastructure → Domain)
        snapshot = await self.vehicle_snapshot_repo.find_by_vehicle_id(vehicle_id)
        
        if not snapshot:
            raise ValueError(f"Vehicle {vehicle_id} not found")
        
        # Step 2: Get historical incidents
        incidents = await self.incident_repo.find_by_vehicle_id(vehicle_id, days_back=90)
        
        # Step 3: Get historical maintenance
        maintenances = await self.maintenance_repo.find_by_vehicle_id(vehicle_id, days_back=90)
        
        # Step 4: Calculate aggregates (Domain Services)
        mttr = MTTRCalculator.calculate_mttr(incidents)
        
        # Step 5: Transform to DTOs
        from ..dto import VehicleSnapshotDTO, IncidentDTO, MaintenanceDTO
        
        snapshot_dto = VehicleSnapshotDTO(
            vehicle_id=snapshot.vehicle_id,
            fleet_location=snapshot.fleet_location,
            status=snapshot.status,
            mileage=snapshot.mileage,
            last_maintenance_date=snapshot.last_maintenance_date,
            incident_count_30days=snapshot.incident_count_30days,
            is_assigned=snapshot.is_assigned,
            captured_at=snapshot.captured_at,
        )
        
        incident_dtos = [
            IncidentDTO(
                incident_id=i.incident_id,
                vehicle_id=i.vehicle_id,
                severity=i.severity,
                description=i.description,
                occurred_at=i.occurred_at,
                resolved_at=i.resolved_at,
                resolution_hours=i.resolution_time_hours(),
            )
            for i in incidents
        ]
        
        maintenance_dtos = [
            MaintenanceDTO(
                maintenance_id=m.maintenance_id,
                vehicle_id=m.vehicle_id,
                maintenance_type=m.maintenance_type,
                description=m.description,
                started_at=m.started_at,
                completed_at=m.completed_at,
                duration_hours=m.duration_hours(),
                cost=m.cost,
            )
            for m in maintenances
        ]
        
        # Step 6: Build response DTO
        return TraceabilityDTO(
            vehicle_id=snapshot.vehicle_id,
            fleet_location=snapshot.fleet_location,
            current_status=snapshot.status,
            total_incidents_lifetime=len(incidents),
            total_incidents_30days=len([i for i in incidents
                                        if (datetime.utcnow() - i.occurred_at).days <= 30]),
            total_maintenance_events=len(maintenances),
            average_mttr_hours=mttr,
            last_snapshot=snapshot_dto,
            recent_incidents=incident_dtos[-5:],  # Last 5 incidents
            recent_maintenances=maintenance_dtos[-5:],  # Last 5 maintenances
        )
