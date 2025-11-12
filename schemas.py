"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Blue Export inquiry schema
class Inquiry(BaseModel):
    """
    Inquiries from potential buyers
    Collection name: "inquiry"
    """
    name: Optional[str] = Field(None, description="Contact person name")
    email: Optional[EmailStr] = Field(None, description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone")
    product_type: str = Field(..., description="Product of interest, e.g., Basmati Rice, Cardamom")
    quantity: str = Field(..., description="Requested quantity and units, e.g., 2 MT, 500 bags")
    destination_country: str = Field(..., description="Destination country for shipment")
    message: Optional[str] = Field(None, description="Additional details or specifications")

class ContactMessage(BaseModel):
    """General contact form submissions
    Collection name: "contactmessage"
    """
    name: str = Field(...)
    email: EmailStr
    phone: Optional[str] = None
    subject: Optional[str] = None
    message: str = Field(...)
