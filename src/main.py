from calculator.calculator import Calculator


def main():
    calc = Calculator()
    print("Welcome to the Calculator!")
    while True:
        operation = input("Enter operation (add, subtract, multiply, divide, power, square_root) or 'exit' to quit: ")
        if operation == 'exit':
            break
        args = list(map(float, input("Enter numbers separated by space: ").split()))
        try:
            result = calc.calculate(operation, *args)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
