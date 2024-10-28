import sys


class InputError(Exception):
    def __init__(self, equation):
        Exception.__init__(self)
        self.equation = equation


def ft_abs(x):
    return x if x > 0 else -x


def ft_sqrt(n, EPS=1E-10):
    # initial guess
    x = 1
    # loop until the difference between the actual guess and the previous guess is less than EPS
    while 1:
        # actual guess is the average of the previous guess and n divided by the previous guess
        nx = (x + n / x) / 2
        if ft_abs(x - nx) < EPS:
            break
        x = nx
    return x


def getDegree(a, b, c):
    if a == 0 and b == 0:
        return 0
    elif a == 0:
        return 1
    else:
        return 2


def discriminant(a, b, c):
    return b * b - 4 * a * c


def format_solution(value):
    rounded_value = round(value, 6)
    return 0 if rounded_value == -0.0 else rounded_value


def constant_solution(c):
    if c == 0:
        print("The equation has any real solution")
    else:
        print("The equation has no solution")
    return


def linear_solution(b, c):
    solution = format_solution(-c / b)
    print("The solution is: {}".format(solution))
    return


def quadratic_solution(a, b, c):
    D = discriminant(a, b, c)
    if D != 0:
        sqrt = ft_sqrt(ft_abs(D))
        real = -b / (2 * a)
        imaginary = sqrt / (2 * a)
        if D > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            print(format_solution(real + imaginary))
            print(format_solution(real - imaginary))
        else:
            print("Discriminant less than zero, the two complex solutions are:")
            print("{0} + {1} * i".format(format_solution(real), format_solution(imaginary)))
            print("{0} - {1} * i".format(format_solution(real), format_solution(imaginary)))
    else:
        print("Discriminant is zero")
        print("The solution is: {}".format(format_solution(-b / (2 * a))))
    return


def parseCoefficients(part, parts):
    a = 0.0
    b = 0.0
    c = 0.0

    for elem in part:
        if elem == '0' or elem == '':
            continue

        if "*" not in elem:
            sys.exit("Error")

        coefficient, var = elem.split('*')
        var, degree = var.split('^')

        # print(f"parts: {parts}")
        # print(f"coefficient: {coefficient}\nvar: {var}\ndegree: {degree}")
        if var != 'X' and var != 'x':
            raise InputError('The variable can only be X or x')

        try:
            if int(degree) == 2:
                a += float(coefficient)
            elif int(degree) == 1:
                b += float(coefficient)
            elif int(degree) == 0:
                c += float(coefficient)
            else:
                if elem not in parts[1]:
                    print("\nPolynomial degree: {0}".format(int(degree)))
                    sys.exit("The polynomial degree is strictly greater than 2, I can't solve.")

        except ValueError:
            raise InputError('Incorrect degree. Must be greater then 0')

    return a, b, c


def parseEquation(equation):
    equation = equation.replace(' ', '').replace('-', '+-').split('=')

    parts = [equation[i].split('+') for i in range(len(equation))]

    if len(parts) != 2:
        raise InputError("An equation has more than one equal sign or none at all")
    for part in parts:
        for term in part:
            if term == '':
                raise InputError("Invalid term in the equation")
    return parts


def calculateCoefficients(equation):
    parts = parseEquation(equation)
    a = 0
    b = 0
    c = 0

    # print(f"parts: {parts}")
    for index, part in enumerate(parts):
        a_tmp, b_tmp, c_tmp = parseCoefficients(part, parts)

        # index = 0 means left side of the equation
        # index = 1 means right side of the equation
        if index == 0:
            a += a_tmp
            b += b_tmp
            c += c_tmp
        else:
            a -= a_tmp
            b -= b_tmp
            c -= c_tmp
    return a, b, c


def display_information(a, b, c, degree):
    print("\nPolynomial degree: {}".format(degree))
    if (a == 0 and b == 0 and c == 0):
        print("Reduced form: 0 = 0")
    elif (a == 0 and b == 0):
        print("Reduced form: {0} * X^0 = 0".format(c))
    elif (a == 0 and c == 0):
        print("Reduced form: {0} * X^1 = 0".format(b))
    elif (b == 0 and c == 0):
        print("Reduced form: {0} * X^2 = 0".format(a))
    elif (a == 0):
        print("Reduced form: {0} * X^1 + {1} * X^0 = 0".format(b, c))
    elif (b == 0):
        print("Reduced form: {0} * X^2 + {1} * X^0 = 0".format(a, c))
    elif (c == 0):
        print("Reduced form: {0} * X^2 + {1} * X^1 = 0".format(a, b))
    else:
        print("Reduced form: {0} * X^2 + {1} * X^1 + {2} * X^0 = 0".format(a, b, c))
    return


def display_solution(a, b, c, degree):
    if degree == 2:
        quadratic_solution(a, b, c)
    elif degree == 1:
        linear_solution(b, c)
    else:
        constant_solution(c)
    return


def solve(equation):
    a, b, c = calculateCoefficients(equation)
    degree = getDegree(a, b, c)

    display_information(a, b, c, degree)
    display_solution(a, b, c, degree)
    return a, b, c


def main():
    try:
        equation = input("Input equation: ")
        solve(equation)
    except KeyboardInterrupt:
        print("\nExiting...")
    except EOFError:
        print("\nExiting...")
    except InputError as i:
        print(f"Error {i}")


if __name__ == "__main__":
    main()