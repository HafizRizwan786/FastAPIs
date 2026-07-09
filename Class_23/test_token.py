"""Test script to find the exact 500 error on /partner/token"""
import asyncio
import traceback

async def main():
    try:
        from database.session import get_session
        from database.models import DeliveryPartner
        from services.delivery_partner import DeliveryPartnerService
        from fastapi import BackgroundTasks
        from passlib.context import CryptContext
        from sqlalchemy import select
        
        password_context = CryptContext(schemes=["bcrypt"])
        
        session_gen = get_session()
        session = await session_gen.__anext__()
        
        # Check if test partner exists
        partner = await session.scalar(
            select(DeliveryPartner).where(DeliveryPartner.email == "testpartner@test.com")
        )
        
        if partner is None:
            print("No test partner found. Creating one directly in DB...")
            from uuid import uuid4
            partner = DeliveryPartner(
                id=uuid4(),
                name="Test Partner",
                email="testpartner@test.com",
                password_hash=password_context.hash("test123"),
                serviceable_zip_code=[12345],
                max_handling_capacity=5,
                email_verified=True,
            )
            session.add(partner)
            await session.commit()
            print(f"Created partner: {partner.id}")
        else:
            print(f"Found existing partner: {partner.id}")
        
        # Now test the token generation
        tasks = BackgroundTasks()
        service = DeliveryPartnerService(session, tasks)
        
        try:
            token = await service.token("testpartner@test.com", "test123")
            print(f"\nSUCCESS! Token: {token}")
        except Exception as e:
            print(f"\nERROR generating token: {type(e).__name__}: {e}")
            traceback.print_exc()
            
    except Exception as e:
        print(f"\nSETUP ERROR: {type(e).__name__}: {e}")
        traceback.print_exc()

asyncio.run(main())
