"""Application Use Case - Generate Availability Charts
Responsabilidad: Generar gráficas de disponibilidad
Capa: Application
"""
from typing import List, Dict
from ..dto import ChartDataDTO
from ...domain.services import ChartGenerator


class GenerateAvailabilityChartsUseCase:
    """Use Case: Generar gráficas de disponibilidad."""
    
    def __init__(self, mongodb_repo):
        self.mongodb_repo = mongodb_repo
    
    async def execute(self, location: str) -> ChartDataDTO:
        """Execute: Generate availability charts."""
        data = await self._fetch_availability_data(location)
        chart = await ChartGenerator.generate_availability_chart(location, data)
        
        return ChartDataDTO(
            chart_id=chart.chart_id,
            chart_type=chart.chart_type,
            title=chart.title,
            data_points=data,
            x_axis_label=chart.x_axis_label,
            y_axis_label=chart.y_axis_label,
        )
    
    async def _fetch_availability_data(self, location: str) -> List[Dict]:
        """Fetch availability data from MongoDB."""
        return []
