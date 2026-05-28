"""Application Use Case - Generate Incident Charts
Responsabilidad: Generar gráficas de incidentes
Capa: Application
"""
from typing import List, Dict
from ..dto import ChartDataDTO
from ...domain.services import ChartGenerator


class GenerateIncidentChartsUseCase:
    """Use Case: Generar gráficas de incidentes."""
    
    def __init__(self, mongodb_repo):
        self.mongodb_repo = mongodb_repo
    
    async def execute(self, location: str) -> ChartDataDTO:
        """Execute: Generate incident charts."""
        data = await self._fetch_incident_data(location)
        chart = await ChartGenerator.generate_incident_chart(location, data)
        
        return ChartDataDTO(
            chart_id=chart.chart_id,
            chart_type=chart.chart_type,
            title=chart.title,
            data_points=data,
            x_axis_label=chart.x_axis_label,
            y_axis_label=chart.y_axis_label,
        )
    
    async def _fetch_incident_data(self, location: str) -> List[Dict]:
        """Fetch incident data from MongoDB."""
        return []
