"""Domain Services - Lógica de negocio que coordina modelos de dominio
Responsabilidad: Calcular métricas según reglas de negocio puras.
Patrón: Strategy Pattern para cálculo de KPIs
Capa: Domain - Lógica de negocio
"""
from typing import List
from datetime import datetime, timedelta
from ..models import VehicleSnapshot, OperationalKPI, Incident, Maintenance


class AvailabilityCalculator:
    """Calcula disponibilidad de flota según reglas de negocio.
    
    Patrón: Strategy Pattern
    Responsabilidad: Encapsular lógica de cálculo de disponibilidad
    """
    
    @staticmethod
    def calculate_availability(
        vehicles: List[VehicleSnapshot],
        location: str
    ) -> OperationalKPI:
        """Calculate availability KPI for a fleet location.
        
        Algoritmo:
        - Total: cantidad de vehículos
        - Disponibles: status == 'DISPONIBLE' AND not is_assigned
        - Porcentaje: (disponibles / total) * 100
        
        Args:
            vehicles: Lista de snapshots de vehículos
            location: Ubicación/sede
            
        Returns:
            OperationalKPI: KPI calculado
        """
        total = len(vehicles)
        available = sum(1 for v in vehicles if v.is_available())
        percentage = (available / total * 100) if total > 0 else 0.0
        
        kpi = OperationalKPI(
            kpi_id=f"KPI-{location}-{datetime.utcnow().strftime('%Y-%m')}",
            fleet_location=location,
            total_vehicles=total,
            available_vehicles=available,
            availability_percentage=percentage,
            average_mttr_hours=0.0,  # Será calculado por MTTRCalculator
            preventive_maintenance_ratio=0.0,  # Será calculado por MaintenanceAnalyzer
            incident_count_month=0,  # Será calculado por IncidentAggregator
        )
        
        return kpi


class MTTRCalculator:
    """Calcula Mean Time To Repair (MTTR) de mantenimientos.
    
    Patrón: Strategy Pattern
    Responsabilidad: Encapsular lógica de cálculo MTTR
    """
    
    @staticmethod
    def calculate_mttr(incidents: List[Incident]) -> float:
        """Calculate Mean Time To Repair from incident resolution times.
        
        Algoritmo:
        - Filtrar incidentes resueltos
        - Calcular tiempo de resolución para cada uno
        - Promediar
        
        Args:
            incidents: Lista de incidentes históricos
            
        Returns:
            float: MTTR en horas
        """
        resolved = [i for i in incidents if i.is_resolved()]
        if not resolved:
            return 0.0
        
        total_hours = sum(i.resolution_time_hours() or 0 for i in resolved)
        return total_hours / len(resolved)


class MaintenanceAnalyzer:
    """Analiza distribución preventiva vs correctiva.
    
    Patrón: Strategy Pattern
    Responsabilidad: Encapsular lógica de análisis de mantenimiento
    """
    
    @staticmethod
    def calculate_preventive_ratio(
        maintenances: List[Maintenance],
        days_lookback: int = 30
    ) -> float:
        """Calculate ratio of preventive to total maintenance.
        
        Algoritmo:
        - Filtrar mantenimientos en período lookback completados
        - Contar preventivos
        - Ratio = preventivos / total
        
        Args:
            maintenances: Lista de registros de mantenimiento
            days_lookback: Días hacia atrás a considerar
            
        Returns:
            float: Ratio entre 0.0 y 1.0
        """
        cutoff = datetime.utcnow() - timedelta(days=days_lookback)
        recent = [m for m in maintenances if m.started_at >= cutoff and m.is_completed()]
        
        if not recent:
            return 0.0
        
        preventive = sum(1 for m in recent if m.is_preventive())
        return preventive / len(recent)


class IncidentAggregator:
    """Agrega estadísticas de incidentes.
    
    Patrón: Aggregator Pattern
    Responsabilidad: Consolidar datos de incidentes en métricas
    """
    
    @staticmethod
    def count_incidents_in_month(
        incidents: List[Incident]
    ) -> int:
        """Count incidents in current month.
        
        Args:
            incidents: Lista de incidentes
            
        Returns:
            int: Cantidad de incidentes este mes
        """
        now = datetime.utcnow()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return sum(1 for i in incidents if i.occurred_at >= month_start)
    
    @staticmethod
    def get_critical_incidents(
        incidents: List[Incident],
        days_back: int = 7
    ) -> List[Incident]:
        """Get critical incidents from recent period.
        
        Args:
            incidents: Lista de incidentes
            days_back: Período a consultar
            
        Returns:
            List[Incident]: Incidentes críticos encontrados
        """
        cutoff = datetime.utcnow() - timedelta(days=days_back)
        return [
            i for i in incidents
            if i.is_critical() and i.occurred_at >= cutoff
        ]
