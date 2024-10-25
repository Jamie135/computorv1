import sys


class InputError(Exception):
    def __init__(self, equation):
        Exception.__init__(self)
        self.equation = equation


def ft_abs(x):
    return x if x > 0 else -x


def ft_sqrt(n, EPS=1E-10):
    x = 1
    while 1:
        nx = (x + n / x) / 2
        if abs(x - nx) < EPS:
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


def constant_solution(c):
    if c == 0:
        print("The equation has any real solution")
    else:
        print("The equation has no solution")
    return


def linear_solution(b, c):
    print("The solution is: {}".format(round(- c / b, 6)))
    return


def quadratic_solution(a, b, c):
    D = discriminant(a, b, c)
    if D != 0:
        sqrt = ft_sqrt(ft_abs(D))
        real = -b / (2 * a)
        imaginary = sqrt / (2 * a)
        if D > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            print(round(real + imaginary, 6))
            print(round(real - imaginary, 6))
        else:
            print("Discriminant less than zero, the two complex solutions are:")
            print("{0} + {1} * i".format(round(real, 6), round(imaginary, 6)))
            print("{0} - {1} * i".format(round(real, 6), round(imaginary, 6)))
    else:
        print("Discriminant is zero")
        print("The solution is: {}".format(round(-b / (2 * a), 6)))
    return


def display_information(a, b, c, degree):
    print("\nPolynomial degree: {}".format(degree))
    print("Reduced form: {0} * X^2 + {1} * X^1 + {2} * X^0 = 0".format(a, b, c))
    return


def parseCoefficients(part):
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
    return parts


def calculateCoefficients(equation):
    parts = parseEquation(equation)
    a = 0
    b = 0
    c = 0

    # print(f"parts: {parts}")
    for index, part in enumerate(parts):
        a_tmp, b_tmp, c_tmp = parseCoefficients(part)

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