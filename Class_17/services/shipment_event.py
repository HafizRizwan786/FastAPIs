from services.base import BaseService
from database.models import ShipmentEvent,Shipment,ShipmentStatus

class ShipmentEventService(BaseService):
    def __init__(self,sessoin):
        super().__init__(ShipmentEvent,sessoin)
        
    async def add(
        self,
        shipment: Shipment,
        location: int=None,
        status: ShipmentStatus=None,
        description: str =None
    )->ShipmentEvent:
        
        if not location or not status:
            latest_event=self.get_latest_event(shipment)
            location=location if location else latest_event.location
            status=status if status else latest_event.status
            
        new_event=ShipmentEvent(
            location=location,
            status=status,
            description=description if description else self._generate_description(status,location),
            shipment=shipment.id,
        )
        return await self._add(new_event)
    
    
    async def get_latest_event(self,shipment: Shipment):
        timeline=shipment.timeline
        timeline.sort(key=lambda event: event.created_at) # sort in the ascending order
        return timeline[-1] # returning the latest event
    
    def _generate_description(self,status: ShipmentStatus,location: int):
        match status:
            case ShipmentStatus.placed:
                return "assigned delivery partner"
            case ShipmentStatus.delivered:
                return "Successfully delivered"
            case ShipmentStatus.out_for_delivery:
                return "Out for delivery"
            case ShipmentStatus.in_transit:
                return f"scanned at {location}"