from pydantic import BaseModel, Field, EmailStr, validator, field_validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

#eNUM - a list of allowed values

class BookGenre(str, Enum):
    """only these book categories are allowed"""
    FICTION = "fiction"
    NON_FICTION = "non_fiction"
    SCIENCE = "science"
    TECHNOLOGY = "technology"
    HISTORY = "history"
    BIOGRAPHY = "biography"
    SELF_HELP = "self_help"

class BookCondition(str, Enum):
    NEW = "new"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    
class Book(BaseModel):
    #defination of book that our api must need follow 
    
    
    #required fields(no default value = required)
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="The title of the book",
        examples="The Great Gatsby"
    )
    
    author: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Author's full name"
    )
    
    isbn: str = Field(
        pattern=  r'^\d{3}-\d{10}$',
        description="ISBN in format: 978-1234567890"
        
    )
    
    genre: BookGenre = Field(
        default= BookGenre.FICTION,
        description= "Book category"
    )
    
    published_year: Optional[int] = Field(
        default= None,
        ge = 1000,  #greater than or equal to 1000
        le = 2026, #less than or equal to 2026
        description= "Year the book was published"
    )
    
    pages: Optional[int] = Field(
        default=None,
        gt= 0,
        description="Number of pages"
    )
    
    price: float = Field(
        default= 0.0,
        gt= 0,
        description="Price of the book"
        
    )
    
    in_stock: bool = Field(
        default= True,
        description= "Is the book available"
    )
    
    tags: List[str] = Field(
        default= [],
        description="Tags for searching"
    ) 
    
    condition: BookCondition = Field(
        default= BookCondition.NEW,
        description="Physical Condition of the book"
    ) 
    
    #custom validator run automatically when data is created
    @field_validator('isbn')
    def validate_isbn(cls, value):
        #to make sure ISBN follows the right format
        
        #remoce any hyphens
        
        clean_isbn =  value.replace("-","")
        
        if len(clean_isbn) != 13: 
            raise ValueError ("ISBN must be 13 digits(with hyphens)")
        
        if not clean_isbn.isdigit():
            raise ValueError("ISBN must  contain only numbers and hyphens")
        
        return value
    @field_validator('published_year')
    def validate_year(cls, value, values):
        """Ensure published year makes sense with other fields"""
        if value and value > 2024:
            raise ValueError('Published year cannot be in the future')
        
        # Can also check against author birth year if we had it
        return value
    
    @field_validator('price')
    def round_price(cls, value):
        """Round price to 2 decimal places"""
        return round(value, 2)
    
    # This tells Pydantic to show an example in docs
    class Config:
        schema_extra = {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "isbn": "978-0743273565",
                "genre": "fiction",
                "published_year": 1925,
                "pages": 180,
                "price": 15.99,
                "in_stock": True,
                "tags": ["classic", "american literature"],
                "condition": "good"
            }
        }

# Response model - What we send back to the client
class BookResponse(Book):
    """This is what we return - includes auto-generated fields"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True  # This allows conversion from database objects

# Update model - For partial updates
class BookUpdate(BaseModel):
    """For updating books - all fields optional"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=2, max_length=100)
    genre: Optional[BookGenre] = None
    published_year: Optional[int] = Field(None, ge=1000, le=2024)
    pages: Optional[int] = Field(None, gt=0)
    price: Optional[float] = Field(None, ge=0)
    in_stock: Optional[bool] = None
    tags: Optional[List[str]] = None
    condition: Optional[BookCondition] = None

# User model for later
class UserCreate(BaseModel):
    """Model for user registration"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern =r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    full_name: str = Field(..., min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=18, le=120)
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    def validate_password_strength(cls, value):
        """Ensure password is strong"""
        if not any(c.isupper() for c in value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in value):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in value):
            raise ValueError('Password must contain at least one number')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in value):
            raise ValueError('Password must contain at least one special character')
        return value
    
    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "full_name": "John Doe",
                "age": 25,
                "password": "SecurePass123!"
            }
        }

class UserResponse(BaseModel):
    """What we send back (NEVER include password!)"""
    id: int
    username: str
    email: str
    full_name: str
    age: Optional[int]
    created_at: datetime