# Test routes
from fastapi import APIRouter

# Create a router for test endpoints
router = APIRouter()

@router.get("/test")
def test_endpoint():
	return "raangus"
