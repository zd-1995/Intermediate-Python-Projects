
'''Geometric shapes calculator and display.
 *** The drawing is pixel-based.'''

# Draw class
class Shape:
    def draw(self):
        pass


# Square class
class square_shape(Shape):
    def __init__(self, side:int):
        self.side = side

    def calculate_area(self):
        return self.side * self.side

    def calculate_perimeter(self):
        return 4 * self.side

    def drawing_shape(self,pen):
        pen.clear()

        for i in range(4):
            pen.forward(self.side)
            pen.right(90)


# Rectangle class
class rectangle_shape(Shape):
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def calculate_area(self):
        return self.length * self.width

    def calculate_perimeter(self):
        return 2 * (self.length + self.width)

    def drawing_shape(self,pen):
        pen.clear()

        for i in range(2):
            pen.forward(self.length)
            pen.right(90)
            pen.forward(self.width)
            pen.right(90)


# Circle class
class circle_shape(Shape):
    def __init__(self, radius: int):
        self.radius = radius

    def calculate_area(self):
        import math
        return math.pi * self.radius ** 2

    def calculate_perimeter(self):
        import math
        return 2 * math.pi * self.radius

    def drawing_shape(self,pen):
        pen.clear()
        pen.begin_fill()
        pen.circle(self.radius)
        pen.end_fill()


# Triangle class



class triangle_shape:
    def __init__(self, base=None, side1=None, side2=None, side3=None,
                 angle1=None, angle2=None, angle_between=None, height=None):
        self.base = base
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
        self.angle1 = angle1  # vertex angle at side2-side3
        self.angle2 = angle2  # vertex angle at side1-side3
        self.angle_between = angle_between  # included angle for SAS
        self.height = height

    ''' There is a validator that checks whether the three given lengths can actually form a valid triangle.'''
    def validate_triangle(self, a, b, c):
        return all(x > 0 for x in (a, b, c)) and a + b > c and a + c > b and b + c > a

    ''' Based on the data entered by the user (side, angle, height, base, etc.), it calculates the remaining missing values.'''
    def calculate_missing(self):
        import math
        # --- SSS ---
        if self.side1 and self.side2 and self.side3:
            if not self.validate_triangle(self.side1, self.side2, self.side3):
                raise ValueError("Invalid side lengths. Cannot form a triangle.")
            self.angle1 = math.degrees(math.acos((self.side2**2 + self.side3**2 - self.side1**2)/(2*self.side2*self.side3)))
            self.angle2 = math.degrees(math.acos((self.side1**2 + self.side3**2 - self.side2**2)/(2*self.side1*self.side3)))
            self.angle_between = 180 - (self.angle1 + self.angle2)
            return

        # --- SAS ---
        if self.side1 and self.side2 and self.angle_between:
            self.side3 = math.sqrt(self.side1**2 + self.side2**2 - 2*self.side1*self.side2*math.cos(math.radians(self.angle_between)))
            self.angle1 = math.degrees(math.asin(self.side1 * math.sin(math.radians(self.angle_between))/self.side3))
            self.angle2 = 180 - self.angle_between - self.angle1
            return

        # --- SSA (two sides + non-included angle) ---
        if self.side1 and self.side2 and self.angle1:
            sin_angle2 = self.side2 * math.sin(math.radians(self.angle1)) / self.side1
            if sin_angle2 > 1 or sin_angle2 < 0:
                raise ValueError("Cannot form a triangle with given SSA parameters.")
            self.angle2 = math.degrees(math.asin(sin_angle2))
            self.angle_between = 180 - self.angle1 - self.angle2
            self.side3 = math.sqrt(self.side1**2 + self.side2**2 - 2*self.side1*self.side2*math.cos(math.radians(self.angle_between)))
            return

        # --- ASA/AAS ---
        if self.base and self.angle1 and self.angle2:
            angle3 = 180 - self.angle1 - self.angle2
            self.side1 = self.base * math.sin(math.radians(self.angle1)) / math.sin(math.radians(angle3))
            self.side2 = self.base * math.sin(math.radians(self.angle2)) / math.sin(math.radians(angle3))
            self.side3 = self.base
            self.angle_between = angle3
            return

        # --- Base + Height ---
        if self.base and self.height:
            self.side1 = math.sqrt((self.base/2)**2 + self.height**2)
            self.side2 = self.side1
            self.side3 = self.base
            self.angle1 = 90
            self.angle2 = math.degrees(math.atan(self.height/(self.base/2)))
            self.angle_between = 180 - self.angle1 - self.angle2
            return

        raise ValueError("Not enough or inconsistent data to define a triangle.")

    def calculate_area(self):
        import math
        if self.base and self.height:
            return 0.5*self.base*self.height
        self.calculate_missing()
        s = (self.side1 + self.side2 + self.side3)/2
        return math.sqrt(s*(s-self.side1)*(s-self.side2)*(s-self.side3))

    def calculate_perimeter(self):
        self.calculate_missing()
        return self.side1 + self.side2 + self.side3

    def drawing_shape(self, pen):
        import math
        self.calculate_missing()
        # place vertices
        A = (0,0)
        B = (self.side3,0)  # base on x-axis
        # calculate C using law of cosines coordinates
        a, b, c = self.side1, self.side2, self.side3
        cos_gamma = (a**2 + b**2 - c**2)/(2*a*b)
        cos_gamma = max(min(cos_gamma,1),-1)
        gamma_rad = math.acos(cos_gamma)
        C = (b * math.cos(gamma_rad), b * math.sin(gamma_rad))

        pen.clear()
        pen.penup()
        pen.goto(A)
        pen.pendown()
        pen.goto(B)
        pen.goto(C)
        pen.goto(A)


def operator_selection():
    while True:
        try:
            selection = int(input("Enter the desired shape number:\n"
                                  "1. Area\n"
                                  "2. Perimeter\n"
                                  "3. Drawing Shape\n"
                                  "4. Exit\n"))

            if selection in [1, 2, 3, 4]:
                return selection
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue


if __name__ == '__main__':
    print("Area and perimeter calculator and geometric shape display system.")

    import turtle
    screen = turtle.Screen()
    screen.title("Geometric Shapes")
    pen = turtle.Turtle()
    pen.color("blue")
    pen.speed(3)

    while True:
        # Display the menu options.
        try:
            selection = int(input("Enter the desired shape number:\n1. Square\n"
                                  "2. Rectangle\n"
                                  "3. Circle \n"
                                  "4. Triangle\n"
                                  "5. Exit\n"
                                  "-  "))

        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        # Select the desired option
        # 1. Square
        if selection == 1:
            # User input data
            side = int(input("Enter the desired side:"))
            # Square object
            shape_square = square_shape(side)
            # choise operation
            while True:
                choice = operator_selection()
                if choice == 1:
                    print(f"The area of the square is {shape_square.calculate_area()}")
                elif choice == 2:
                    print(f"The perimeter of the square is {shape_square.calculate_perimeter()}")
                elif choice == 3:
                    shape_square.drawing_shape(pen)
                elif choice == 4:
                    break

        # 2. Rectangle
        elif selection == 2:
            # User input data
            length = int(input("Enter the desired length:"))
            width = int(input("Enter the desired width:"))
            # Rectangle object
            shape_rectangle = rectangle_shape(length, width)
            # choise operation
            while True:
                choice = operator_selection()
                if choice == 1:
                    print(f"The area of the rectangle is {shape_rectangle.calculate_area()}")
                elif choice == 2:
                    print(f"The perimeter of the rectangle is {shape_rectangle.calculate_perimeter()}")
                elif choice == 3:
                    shape_rectangle.drawing_shape(pen)
                elif choice == 4:
                    break

        # 3. Circle
        elif selection == 3:
            # User input data
            radius = int(input("Enter the desired radius:"))
            # Circle object
            shape_circle = circle_shape(radius)
            # choise operation
            while True:
                choice = operator_selection()
                if choice == 1:
                    print(f"The area of the circle is {shape_circle.calculate_area()}")
                elif choice == 2:
                    print(f"The perimeter of the circle is {shape_circle.calculate_perimeter()}")
                elif choice == 3:
                    shape_circle.drawing_shape(pen)
                elif choice == 4:
                    break


        # 4. Triangle
        elif selection == 4:
            print("Please enter the known triangle parameters.")
            print("* If you don't know a value, leave it blank and press Enter. You must enter at least 2 values.")
            print("Tip: If you know two sides and the included angle, enter it as 'angle between'\n.")

            # User input data
            height = input("Enter the desired height (press Enter to skip): ")
            base = input("Enter the desired base (press Enter to skip): ")
            side1 = input("Enter the desired side1 (press Enter to skip): ")
            side2 = input("Enter the desired side2 (press Enter to skip): ")
            side3 = input("Enter the desired side3 (press Enter to skip): ")
            angle1 = input("Enter the desired angle1 (degrees, press Enter to skip): ")
            angle2 = input("Enter the desired angle2 (degrees, press Enter to skip): ")
            angle_between = input("Enter the angle between two sides (degrees, press Enter to skip): ")


            # Convert to numbers if provided
            def to_number(val):
                try:
                    return float(val) if val else None
                except:
                    return None

            height = to_number(height)
            base = to_number(base)
            side1 = to_number(side1)
            side2 = to_number(side2)
            side3 = to_number(side3)
            angle1 = to_number(angle1)
            angle2 = to_number(angle2)
            angle_between = to_number(angle_between)

            # Triangle object
            shape_triangle = triangle_shape(
                base=base,
                side1=side1,
                side2=side2,
                side3=side3,
                angle1=angle1,
                angle2=angle2,
                angle_between=angle_between,
                height=height
            )

            # choise operation
            while True:
                choice = operator_selection()
                if choice == 1:
                    print(f"The area of the triangle is {shape_triangle.calculate_area():.2f}")
                elif choice == 2:
                    print(f"The perimeter of the triangle is {shape_triangle.calculate_perimeter():.2f}")
                elif choice == 3:
                    shape_triangle.drawing_shape(pen)
                elif choice == 4:
                    break


        # 5. Exit
        elif selection == 5:
            screen.bye()
            break

    screen.mainloop()