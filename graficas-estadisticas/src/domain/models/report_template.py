"""Domain Model - Report Template
Responsabilidad: Template para renderizado de reportes
Patrón: Domain Model
Capa: Domain
"""
from typing import Dict, List, Optional
from pydantic import BaseModel


class ReportTemplate(BaseModel):
    """Template para renderización de reportes.
    
    Responsabilidad: Definir estructura de un template de reporte
    """
    
    template_id: str
    template_name: str
    template_file: str  # Ruta al archivo Jinja2
    sections: List[str]  # ["header", "metrics", "charts", "footer"]
    variables: Dict[str, str]  # Variables que requiere el template
    
    class Config:
        json_schema_extra = {
            "example": {
                "template_id": "TPL-EXEC-001",
                "template_name": "Executive Report Template",
                "template_file": "templates/report_template.html",
                "sections": ["header", "metrics", "charts", "footer"],
                "variables": {
                    "report_title": "string",
                    "period_start": "datetime",
                    "period_end": "datetime",
                    "location": "string"
                }
            }
        }
