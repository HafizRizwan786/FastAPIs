from services.base import BaseService
from database.models import ShipmentEvent,Shipment,ShipmentStatus

class ShipmentEventService(BaseService):
    def __init__(self,session):
        super().__init__(ShipmentEvent,session)
        
    async def add(
        self,
        shipment: Shipment,
        location: int=None,
        status: ShipmentStatus=None,
        description: str =None
    )->ShipmentEvent:
        
        if location is None or status is None:
            latest_event=await self.get_latest_event(shipment)
            if latest_event is not None:
                location=location if location is not None else latest_event.location
                status=status if status is not None else latest_event.status
            else:
                raise ValueError("Cannot create first shipment event without both location and status")
            
        new_event=ShipmentEvent(
            location=location,
            status=status,
            description=description if description else self._generate_description(status,location),
            shipment_id=shipment.id,
        )
        return await self._add(new_event)
    
    
    async def get_latest_event(self,shipment: Shipment):
        timeline=shipment.timeline
        if not timeline:
            return None
        timeline.sort(key=lambda event: event.created_at)
        return timeline[-1]
    
    
    def _generate_description(self,status: ShipmentStatus,location: int):
        match status:
            case ShipmentStatus.placed:
                return "assigned delivery partner"
            case ShipmentStatus.delivered:
                return "Successfully delivered"
            case ShipmentStatus.out_for_delivery:
                return "Out for delivery"
            case ShipmentStatus.cancelled:
                return "Cancelled by seller"
            case ShipmentStatus.in_transit:
                return f"scanned at {location}"