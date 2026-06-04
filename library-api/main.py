


from fastapi import FastAPI

#creating app object
app = FastAPI(
    title= "First API",
    description= "Learning FastAPI",
    version= "1.0.0"
)

#creating endpoints
@app.get("/")
async def root():
    return {
        "message":"Welcome to my Fast API",
        "status":"running",
        "tips": [
            "docs",
            "redoc",
            "greeting"
        ]
    }
    
#path parameter example
@app.get("/hello/{name}")
async def say_hello(name:str):
    return {
        "greeting": f"Hello, {name}!",
        "your_name_uppercase": name.upper(),
        "name_length": len(name)
    }
    
#query parameter  example
@app.get("/greet")
async def greet_user(name: str = "Guest", age: int=0):
    #Try: /greet?name=John&age=25
    if age<18:
        message = f"Hello young {name}!"
    else: 
        message = f"Hello {name}, you're an adult!"
    
    return {
        "message":message,
        "name": name,
        "age": age
    }
    
#multiple path parameters
@app.get("/calculate/{num1}/{num2}")
async def calculate(num1: float, num2:float, operation: str="add"):
       #try: /calculate/5/10?operation=multiply
    operations  = {
        "add": num1+num2,
        "subtract": num1-num2,
        "multiply": num1*num2,
        "divide": num1/num2 if num2!=0 else "Cannot divide by zero"
        }
    result = operations.get(operation, "invalid operation")
        
    return {
        "num1":num1,
        "num2":num2,
        "operation":operation,
        "result": result
            }
    
#return current date and time
@app.get("/time")
async def current_time():
    from datetime import datetime
    return {
        "current_time": datetime.now().isoformat(),
        "timestamp": datetime.now().timestamp()
    }
    
    
#CHECK IF THE NUMBER IS EVEN
@app.get("/is_even/{number}")
async def check_even(number: int):
    return {
        "number": number,
        "is_even": number % 2 == 0,
        "explanation": f"{number} is {'even' if number % 2 == 0 else 'odd'}"
        
    }
    
#reverse a text string
@app.get("/reverse_text")
async def reverse_text(text: str = 'hello'):
    return {
        "original": text,
        "reversed": text[::-1],
        "length": len(text)
    }