"""gRPC Contracts Specification
Documentación de servicios gRPC
"""

# Vehicle Service

```
service VehicleService {
    rpc GetVehicle(VehicleRequest) returns (VehicleResponse);
    rpc ListVehicles(ListRequest) returns (VehicleList);
}
```

Responsabilidad: Proporcionar datos de vehículos

---

# Incident Service

```
service IncidentService {
    rpc GetIncidents(IncidentRequest) returns (IncidentList);
    rpc CreateIncident(CreateIncidentRequest) returns (IncidentResponse);
}
```

Responsabilidad: Gestionar incidentes de flota

---

# Assignment Service

```
service AssignmentService {
    rpc GetAssignments(AssignmentRequest) returns (AssignmentList);
}
```

Responsabilidad: Gestionar asignaciones de vehículos

---

# Maintenance Service

```
service MaintenanceService {
    rpc GetMaintenanceRecords(MaintenanceRequest) returns (MaintenanceList);
}
```

Responsabilidad: Gestionar mantenimientos
