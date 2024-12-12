from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from typing import Optional, Dict
from decimal import Decimal, ROUND_HALF_UP

app = FastAPI()
templates = Jinja2Templates(directory="core")

def calculate_cleaning_cost(type1: Decimal, area: Decimal, rate: Decimal, discount: Decimal) -> Decimal:
    base_cost = area * 3 * rate
    discount_amount = base_cost * (discount / 100)
    total_cost = ((base_cost - discount_amount) * (type1 + 100)/100).quantize(Decimal("0.00"), ROUND_HALF_UP) # Round to 2 decimal places
    return total_cost


@app.post("/calculate")
async def calculate(request: Request, type1: Decimal = Form(...), area: Decimal = Form(...), rate: Decimal = Form(...), discount: Decimal = Form(0), disinfection: Optional[bool] = Form(False), window_cleaning: Optional[bool] = Form(False)):
    services = {
        "disinfection": Decimal(500) if disinfection else Decimal(0),
        "window_cleaning": Decimal(300) if window_cleaning else Decimal(0)
    }
    total_cost = calculate_cleaning_cost(type1, area, rate, discount)
    return templates.TemplateResponse("Calculator.html", {"request": request, "total_cost": total_cost, "area": area, "rate": rate, "discount": discount})


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("Calculator.html", {"request": request, "total_cost": None})