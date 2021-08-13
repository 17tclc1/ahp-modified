from fractions import Fraction
import numpy as np

criterions = ['Effect', 'Plot', 'Character']
alternatives = ['Avenger', 'Captain Marvel', 'Justice league']

# Generate pair wise comparison matrix
def pair_wise_comparison(units):
    n = len(units)
    pair_wise_matrix = np.zeros((n, n))
    for i in range(0, n):
        for j in range(i, n):
            if i == j:
                scale = 1
            else:
                scale = float(Fraction(input(units[i] + ' to ' + units[j] + ': ')))
            pair_wise_matrix[i][j] = scale
            pair_wise_matrix[j][i] = float(1 / scale)
    return pair_wise_matrix

# Generate weight vector for matrix
def get_weight_vector(matrix):
    sum_all_column = np.array(np.matrix(matrix).sum(axis=0)).flatten()
    normalize_matrix = matrix / np.array(sum_all_column)

    sum_all_row = np.array(np.matrix(normalize_matrix).sum(axis=1)).flatten()
    return sum_all_row / sum(sum_all_row)


# Generate consistency ratio
def find_consistency_ratio(matrix, weight_vector):
    weighted_sum_vector = np.dot(weight_vector, matrix.T)
    consistency_vector = weighted_sum_vector / weight_vector

    n = len(weight_vector)
    lambda_value = sum(consistency_vector) / n
    # Consistency index
    CI = (lambda_value - n) / (n - 1)
    # Look-up table for RI[n]
    RI = {
        1: 0,
        2: 0,
        3: 0.58,
        4: 0.9,
        5: 1.12,
        6: 1.24,
        7: 1.32,
        8: 1.41
    }
    CR = CI / RI[n]
    return CR

def calculate_weight_and_matrix(matrix):
    compare_matrix = pair_wise_comparison(matrix)
    weight_vector = get_weight_vector(compare_matrix)
    print("Pair wise comparison matrix:")
    print(compare_matrix)
    print("Weight vector: ")
    print(weight_vector)
    CR = find_consistency_ratio(compare_matrix, weight_vector)
    print("Consistency ratio = " + str(CR))
    if CR >= 0.1:
        print("Consistency check failed, please try again")
        return calculate_weight_and_matrix(matrix)
    else:
        print("Consistency check successfully")
        return compare_matrix, weight_vector
###################################################################################
### Start program
###################################################################################

compare_criteria_matrix, criteria_weight = calculate_weight_and_matrix(criterions)

# Find weight using private vector method
print(criteria_weight)

alternative_weight_matrix = []
for i in range(len(criterions)):
    print("Consider criteria " + str(criterions[i]))
    # Calculate alternative_weight of each alternative
    compare_alternative_matrix, alternative_weight = calculate_weight_and_matrix(alternatives)
    # Push weight to array
    alternative_weight_matrix.append(alternative_weight)
print(np.array(alternative_weight_matrix))
factor_evaluation = np.dot(np.array(alternative_weight_matrix).T, criteria_weight)
print("Factor evaluation: ")
print(factor_evaluation)
print("Based on AHP, the best option would be: " + alternatives[np.argmax(factor_evaluation)])