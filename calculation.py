def is_equidistant(x_values, tolerance=1e-6):
    if len(x_values) < 2:
        return True
    h = x_values[1] - x_values[0]
    for i in range(2, len(x_values)):
        if abs((x_values[i] - x_values[i - 1]) - h) > tolerance:
            return False
    return True


def compute_differences(x, y):
    n = len(x)
    table = [[x[i], y[i]] + [None] * (n - 1) for i in range(n)]

    if is_equidistant(x):
        # Конечные разности для равноотстоящих узлов
        for order in range(1, n):
            for i in range(n - order):
                table[i][order + 1] = table[i + 1][order] - table[i][order]
    else:
        # Разделенные разности для неравноотстоящих
        for order in range(1, n):
            for i in range(n - order):
                table[i][order + 1] = (table[i + 1][order] - table[i][order]) / (x[i + order] - x[i])

    return table


def lagrange_interpolation(x_values, y_values, x):
    n = len(x_values)
    result = 0.0
    for i in range(n):
        term = y_values[i]
        for j in range(n):
            if j != i:
                term *= (x - x_values[j]) / (x_values[i] - x_values[j])
        result += term
    return result


def newton_divided_differences(x_values, y_values, x):
    n = len(x_values)
    coef = y_values.copy()

    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coef[i] = (coef[i] - coef[i - 1]) / (x_values[i] - x_values[i - j])

    return evaluate_newton_divided(x_values, coef, x)


def evaluate_newton_divided(x_values, coefficients, x):
    n = len(coefficients)
    result = coefficients[-1]
    for i in range(n - 2, -1, -1):
        result = result * (x - x_values[i]) + coefficients[i]
    return result


def newton_forward_difference(x_values, y_values, x):
    if not is_equidistant(x_values):
        return newton_divided_differences(x_values, y_values, x)

    n = len(x_values)
    h = x_values[1] - x_values[0]
    t = (x - x_values[0]) / h

    # Строим таблицу конечных разностей
    diff_table = [y_values.copy()]
    for i in range(1, n):
        diff_table.append([diff_table[i - 1][j + 1] - diff_table[i - 1][j] for j in range(n - i)])

    result = diff_table[0][0]
    product = 1.0
    for i in range(1, n):
        product *= (t - (i - 1)) / i
        result += product * diff_table[i][0]

    return result


def newton_backward_difference(x_values, y_values, x):
    if not is_equidistant(x_values):
        return newton_divided_differences(x_values, y_values, x)

    n = len(x_values)
    h = x_values[1] - x_values[0]
    t = (x - x_values[-1]) / h

    # Строим таблицу конечных разностей
    diff_table = [y_values.copy()]
    for i in range(1, n):
        diff_table.append([diff_table[i - 1][j + 1] - diff_table[i - 1][j] for j in range(n - i)])

    result = diff_table[0][-1]
    product = 1.0
    for i in range(1, n):
        product *= (t + (i - 1)) / i
        result += product * diff_table[i][-1]

    return result