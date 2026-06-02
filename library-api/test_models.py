# Create test_models.py
"""
TEST the MODELS - See validation in action!
Run: python test_models.py
"""

from models import Book, BookGenre, BookCondition, UserCreate
from pydantic import ValidationError

# Test 1: Valid Book
print("=" * 50)
print("TEST 1: Creating a valid book")
print("=" * 50)

try:
    valid_book = Book(
        title="Python Programming",
        author="John Smith",
        isbn="978-1234567890",
        genre=BookGenre.TECHNOLOGY,
        published_year=2023,
        pages=500,
        price=49.99,
        tags=["python", "programming", "beginner"]
    )
    print("Valid book created successfully!")
    print(f"Book details: {valid_book}")
except ValidationError as e:
    print(f" Validation failed: {e}")

# Test 2: Invalid Book (too short title)
print("\n" + "=" * 50)
print("TEST 2: Creating invalid book (short title)")
print("=" * 50)

try:
    invalid_book = Book(
        title="",  # Too short!
        author="JS",
        isbn="not-valid-isbn",
        published_year=3000  # Future year!
    )
except ValidationError as e:
    print("Correctly rejected invalid book!")
    print("Validation errors:")
    for error in e.errors():
        print(f"  - {error['loc'][0]}: {error['msg']}")

# Test 3: Valid User
print("\n" + "=" * 50)
print("TEST 3: Creating valid user")
print("=" * 50)

try:
    valid_user = UserCreate(
        username="john_doe",
        email="john@example.com",
        full_name="John Doe",
        age=25,
        password="SecurePass123!"
    )
    print("Valid user created!")
    # Note: Password is in the object but would be hashed before storing
except ValidationError as e:
    print(f"❌ Failed: {e}")

# Test 4: Weak Password
print("\n" + "=" * 50)
print("TEST 4: User with weak password")
print("=" * 50)

try:
    weak_user = UserCreate(
        username="test_user",
        email="test@example.com",
        full_name="Test User",
        password="weak"  # Too simple!
    )
except ValidationError as e:
    print("Correctly rejected weak password!")
    for error in e.errors():
        print(f"  - {error['msg']}")