from pydantic import BaseModel, Field
from typing import List, Optional

class FarmerProfile(BaseModel):
    user_id: str
    location: Optional[str] = "Unknown"
    soil_type: Optional[str] = "General"
    primary_crops: List[str] = Field(default_factory=list)
    irrigation_type: Optional[str] = "Rain-fed"
    
    class Config:
        populate_by_name = True
