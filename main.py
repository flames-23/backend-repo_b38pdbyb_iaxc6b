import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from schemas import Inquiry, ContactMessage
from database import create_document

app = FastAPI(title="Blue Export API", description="Backend for Blue Export website")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Blue Export backend is running"}

@app.get("/api/products")
def get_products() -> Dict[str, Any]:
    """Return product catalog for rice and spices"""
    rice = [
        {
            "name": "Basmati Rice",
            "origin": "India/Pakistan",
            "grain_length": "Long grain",
            "moisture": "12-13%",
            "broken": "<2%",
            "image": "https://images.unsplash.com/photo-1546549039-49ec6f7b71a6?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Sona Masoori",
            "origin": "India",
            "grain_length": "Medium grain",
            "moisture": "12-13%",
            "broken": "<5%",
            "image": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Ponni Rice",
            "origin": "India",
            "grain_length": "Medium grain",
            "moisture": "12-13%",
            "broken": "<5%",
            "image": "https://images.unsplash.com/photo-1536305030432-2a9fb3b86f30?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Matta Rice",
            "origin": "India (Kerala)",
            "grain_length": "Medium grain, parboiled",
            "moisture": "12-13%",
            "broken": "<3%",
            "image": "https://images.unsplash.com/photo-1604908554027-7748ac15f8f5?q=80&w=1200&auto=format&fit=crop"
        }
    ]

    spices = [
        {
            "name": "Cardamom",
            "grade": "7-8mm, bold",
            "admixture": "<1%",
            "image": "https://images.unsplash.com/photo-1624860452965-09237b04a647?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Cloves",
            "grade": "Hand-picked",
            "admixture": "<2%",
            "image": "https://images.unsplash.com/photo-1640020483527-e29b28c70c61?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Cinnamon",
            "grade": "Quills, 8cm+",
            "admixture": "<1%",
            "image": "https://images.unsplash.com/photo-1519680772-8b3256f05fe0?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Black Pepper",
            "grade": "FAQ/ASTA",
            "admixture": "<1%",
            "image": "https://images.unsplash.com/photo-1560785496-3c9d27877182?q=80&w=1200&auto=format&fit=crop"
        },
        {
            "name": "Cumin",
            "grade": "99% purity",
            "admixture": "<1%",
            "image": "https://images.unsplash.com/photo-1587049352851-c9e6fafe05f0?q=80&w=1200&auto=format&fit=crop"
        }
    ]

    return {"rice": rice, "spices": spices}

@app.post("/api/inquiry")
def submit_inquiry(payload: Inquiry) -> Dict[str, str]:
    """Accept inquiry form submissions and store in database"""
    try:
        doc_id = create_document("inquiry", payload)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact")
def submit_contact(payload: ContactMessage) -> Dict[str, str]:
    """Accept contact messages and store in database"""
    try:
        doc_id = create_document("contactmessage", payload)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
