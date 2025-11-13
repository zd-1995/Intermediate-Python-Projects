# Intermediate Python Projects

This repository contains intermediate Python projects for practice and learning. It includes:

1 - **Library management**

2 - **Geometric Shapes Calculator and Drawer**

---

## Files in this project

### 1. `Library_management.py`
A simple **Python Object-Oriented Library Management System** that allows users to manage books and members, including adding, removing, renting, and returning books. 
- Add and remove books
- Search for books by ID, title, author, or year published
- Register and delete users
- Check membership status (`member` or `employee`)
- Rent and return books
- Prevent duplicate user registration by national code
- Console-based interactive menu

### 2. `Geometric_shape_calculator.py`

A **Python-based geometric shape calculator** that can compute **area**, **perimeter**, and **draw** different shapes using the `turtle` graphics module.

**Features**

Supports four geometric shapes:
- **Square**
- **Rectangle**
- **Circle**
- **Triangle** (multiple calculation modes)

Each shape can:
- Calculate **area**
- Calculate **perimeter**
- **Draw** itself on a Turtle graphics window

**Triangle Calculation Logic**

The `triangle_shape` class supports multiple ways to define a triangle:

| Input Type | Description |
|-------------|--------------|
| **SSS** | Three sides |
| **SAS** | Two sides and included angle |
| **SSA** | Two sides and non-included angle |
| **ASA / AAS** | Two angles and one side |
| **Base + Height** | Base length and height |

The class automatically detects which case applies and computes the remaining sides and angles.

It also includes:
- `validate_triangle(a, b, c)` → Checks triangle inequality  
- `calculate_missing()` → Fills in all missing sides/angles based on provided data  
- `calculate_area()` → Uses Heron’s formula or base×height/2  
- `calculate_perimeter()` → Sum of all sides  

**Turtle Drawing Logic**

Each shape has its own `drawing_shape(pen)` method.  
The Turtle window (`turtle.Screen()`) is created **only once** in the program.  

---

** All code files are executed only by running in the Python environment.

This project was developed and tested with the following versions:

- **Python**: 3.13.5