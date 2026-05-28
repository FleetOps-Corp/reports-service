"""Domain Services - Business Logic
Responsabilidad: Implementar lógica de negocio de dominio
Patrón: Domain Service, Strategy Pattern, Aggregator Pattern
Capa: Domain Layer
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from .models import Incident, Maintenance, OperationalKPI


class AvailabilityCalculator:
    """Calcula disponibilidad de flota.
    
    Patrón: Strategy Pattern
    Responsabilidad: Encapsular lógica de cálculo de disponibilidad
    """
    
    @staticmethod
    async def calculate_availability(
        incidents: List[Incident],
        maintenance: List[Maintenance],
        period_hours: int = 720  # 30 días por defecto
    ) -> float:
        """Calculate fleet availability percentage.
        
        Fórmula: (Total Hours - Downtime Hours) / Total Hours * 100
        
        Args:
            incidents: Lista de incidentes en período
            maintenance: Lista de mantenimientos en período
            period_hours: Horas totales del período
            
        Returns:
            float: Porcentaje de disponibilidad (0-100)
        """
        downtime_hours = 0.0
        
        for incident in incidents:
            if incident.resolution_date:
                downtime = (incident.resolution_date - incident.created_at).total_seconds() / 3600
                downtime_hours += downtime
        
        for maint in maintenance:
            if maint.end_time:
                downtime = (maint.end_time - maint.start_time).total_seconds() / 3600
                downtime_hours += downtime
        
        availability = ((period_hours - downtime_hours) / period_hours) * 100
        return max(0, min(100, availability))  # Clamp 0-100


class MTTRCalculator:
    """Calcula MTTR (Mean Time To Repair).
    
    Patrón: Domain Service
    Responsabilidad: Cálculo de métricas de reparación
    """
    
    @staticmethod
    async def calculate_mttr(incidents: List[Incident]) -> float:
        """Calculate Mean Time To Repair.
        
        Args:
            incidents: Lista de incidentes resueltos
            
        Returns:
            float: MTTR en horas
        """
        if not incidents:
            return 0.0
        
        resolved_incidents = [
            i for i in incidents
            if i.resolution_date and i.severity != "PREVENTIVO"
        ]
        
        if not resolved_incidents:
            return 0.0
        
        total_time = sum(
            (i.resolution_date - i.created_at).total_seconds() / 3600
            for i in resolved_incidents
        )
        
        return total_time / len(resolved_incidents)


class IncidentAggregator:
    """Agrega y analiza incidentes.
    
    Patrón: Aggregator Pattern
    Responsabilidad: Consolidar análisis de incidentes
    """
    
    @staticmethod
    async def get_incident_distribution(
        incidents: List[Incident]
    ) -> Dict[str, int]:
        """Get distribution of incidents by severity.
        
        Args:
            incidents: Lista de incidentes
            
        Returns:
            Dict: Conteo por severidad
        """
        distribution = {
            "CRITICA": 0,
            "ALTA": 0,
            "MEDIA": 0,
            "BAJA": 0,
        }
        
        for incident in incidents:
            severity = incident.severity
            if severity in distribution:
                distribution[severity] += 1
        
        return distribution
    
    @staticmethod
    async def get_recurrent_failures(
        incidents: List[Incident],
        min_occurrences: int = 2
    ) -> Dict[str, int]:
        """Identify recurrent failure patterns.
        
        Args:
            incidents: Lista de incidentes
            min_occurrences: Mínimo de ocurrencias para considerar recurrente
            
        Returns:
            Dict: Problemas recurrentes y conteo
        """
        failure_types = {}
        
        for incident in incidents:
            problem = incident.problem_description
            if problem:
                failure_types[problem] = failure_types.get(problem, 0) + 1
        
        return {
            k: v for k, v in failure_types.items()
            if v >= min_occurrences
        }


class MaintenanceAnalyzer:
    """Analiza patrones de mantenimiento.
    
    Patrón: Domain Service
    Responsabilidad: Análisis de mantenimiento preventivo vs correctivo
    """
    
    @staticmethod
    async def calculate_preventive_ratio(
        maintenances: List[Maintenance]
    ) -> float:
        """Calculate preventive maintenance ratio.
        
        Fórmula: Preventive / (Preventive + Corrective)
        
        Args:
            maintenances: Lista de registros de mantenimiento
            
        Returns:
            float: Ratio 0-1
        """
        if not maintenances:
            return 0.0
        
        preventive_count = sum(
            1 for m in maintenances
            if m.maintenance_type == "PREVENTIVO"
        )
        
        return preventive_count / len(maintenances)
    
    @staticmethod
    async def get_maintenance_distribution(
        maintenances: List[Maintenance]
    ) -> Dict[str, int]:
        """Get distribution of maintenance by type.
        
        Args:
            maintenances: Lista de registros
            
        Returns:
            Dict: Conteo por tipo
        """
        distribution = {
            "PREVENTIVO": 0,
            "CORRECTIVO": 0,
        }
        
        for maint in maintenances:
            maint_type = maint.maintenance_type
            if maint_type in distribution:
                distribution[maint_type] += 1
        
        return distribution
