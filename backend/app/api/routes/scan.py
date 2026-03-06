from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.database import get_db
from app.db.models import PendingDevice, ScanRun
from app.schemas.scan import PendingDeviceResponse, ScanRunResponse

router = APIRouter()


@router.post("/trigger", response_model=ScanRunResponse)
async def trigger_scan(db: AsyncSession = Depends(get_db), _: str = Depends(get_current_user)):
    run = ScanRun(status="running", ranges=[])
    db.add(run)
    await db.commit()
    await db.refresh(run)
    # TODO: launch scanner in background thread
    return run


@router.get("/pending", response_model=list[PendingDeviceResponse])
async def list_pending(db: AsyncSession = Depends(get_db), _: str = Depends(get_current_user)):
    result = await db.execute(select(PendingDevice).where(PendingDevice.status == "pending"))
    return result.scalars().all()


@router.post("/pending/{device_id}/approve")
async def approve_device(device_id: str, db: AsyncSession = Depends(get_db), _: str = Depends(get_current_user)):
    device = await db.get(PendingDevice, device_id)
    if device:
        device.status = "approved"
        await db.commit()
    return {"approved": True}


@router.post("/pending/{device_id}/hide")
async def hide_device(device_id: str, db: AsyncSession = Depends(get_db), _: str = Depends(get_current_user)):
    device = await db.get(PendingDevice, device_id)
    if device:
        device.status = "hidden"
        await db.commit()
    return {"hidden": True}
