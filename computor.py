import sys


def format_solution(value):
    rounded_value = round(value, 6)
    return 0 if rounded_value == -0.0 else rounded_value


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


def discriminant(a, b, c):
    return b * b - 4 * a * c


def constant_solution(c):
    if c == 0:
        print("The equation has any real number solution")
    else:
        print("The equation has no solution")
    return


def linear_solution(b, c):
    solution = format_solution(-c / b)
    print(f"The solution is:\n{solution}")
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
            print("Discriminant is strictly negative, the two complex solutions are:")
            print("{0} + {1} * i".format(format_solution(real), format_solution(imaginary)))
            print("{0} - {1} * i".format(format_solution(real), format_solution(imaginary)))
    else:
        print("Discriminant is zero")
        print("The solution is: {}".format(format_solution(-b / (2 * a))))
    return


def display_solution(a, b, c, degree):
    if degree == 2:
        quadratic_solution(a, b, c)
    elif degree == 1:
        linear_solution(b, c)
    else:
        constant_solution(c)
    return


def display_reduced(reduced_coefficient):
    terms = []
    for degree in reduced_coefficient:
        coefficient = reduced_coefficient[degree]
        if coefficient == 0 and len(reduced_coefficient) > 1:
            continue
        else:
            terms.append(f"{coefficient} * X^{degree}")
    
    reduced_form = " + ".join(terms).replace("+ -", "- ")
    print(f"\nReduced form: {reduced_form} = 0")


def getCoefficientByDegree(reduced_coefficient):
    a = 0
    b = 0
    c = 0
    degree = 0
    for deg in reduced_coefficient:
        if reduced_coefficient[deg] != 0:
            if degree < deg:
                degree = deg
            if deg == 2:
                a = reduced_coefficient[deg]
            elif deg == 1:
                b = reduced_coefficient[deg]
            elif deg == 0:
                c = reduced_coefficient[deg]
    return a, b, c, degree


def parseCoefficients(term):
    coefficients_dict = {}
    counted_degrees = []

    for elem in term:
        # print(f"\nterm: {term}\nelem: {elem}")
        if (elem[0] == '0' and len(elem) > 1) or elem == '':
            continue
        if "*" not in elem or "^" not in elem:
            sys.exit("Error: Invalid term in the equation")

        coefficient, var = elem.split('*')
        var, degree = var.split('^')

        # print(f"\ncoefficient: {coefficient}\nvar: {var}\ndegree: {degree}")
        if var != 'X' and var != 'x':
            sys.exit("Error: The variable can only be X")

        try:
            degree = int(degree)
            if degree not in counted_degrees:
                coefficients_dict[degree] = 0.0
                counted_degrees.append(degree)
            coefficient = float(coefficient)
            coefficients_dict[degree] += coefficient

        except ValueError:
            sys.exit("Error: Invalid terms in the equation")

    return coefficients_dict


def parseEquation(equation):
    equation = equation.replace(' ', '').replace('-', '+-').split('=')

    terms = [equation[i].split('+') for i in range(len(equation))]

    if len(terms) != 2:
        sys.exit("Error: An equation must have exactly one equal sign")
    for term in terms:
        for term in term:
            if term == '':
                sys.exit("Error: Invalid term in the equation")
    return terms


def calculateCoefficients(equation):
    terms = parseEquation(equation)
    reduced_coefficients = {}

    # print(f"\nterms: {terms}")
    for index, term in enumerate(terms):
        if index == 0:
            left_coefficients = dict(sorted(parseCoefficients(term).items(), reverse=True))
        else:
            right_coefficients = dict(sorted(parseCoefficients(term).items(), reverse=True))

    degree_union = set(left_coefficients.keys()).union(set(right_coefficients.keys()))
    # print(f"\nUnion: {degree_union}")

    # for each degree, get either the value at that degree or 0 if it doesn't exist
    for degree in degree_union:
        left_value = left_coefficients.get(degree, 0)
        right_value = right_coefficients.get(degree, 0)
        reduced_coefficients[degree] = left_value - right_value

    return dict(sorted(reduced_coefficients.items(), reverse=True))


def solve(equation):
    reduced_coefficient = calculateCoefficients(equation)
    # print("\nReduced coefficients: {0}".format(reduced_coefficient))

    a, b, c, degree = getCoefficientByDegree(reduced_coefficient)
    # print("degree: {0}".format(degree))

    display_reduced(reduced_coefficient)
    print(f"Polynomial degree: {degree}")
    if degree > 2:
        print("The polynomial degree is stricly greater than 2, I can't solve.")
    else:
        display_solution(a, b, c, degree)
    return


def main():
    try:
        equation = input("Input equation: ")
        solve(equation)
    except KeyboardInterrupt:
        print("\nExiting...")
    except EOFError:
        print("\nExiting...")


if __name__ == "__main__":
    main()