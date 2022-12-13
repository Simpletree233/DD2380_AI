#TODO: add dimension and space between the output elements


def main():
    # Split the line into a list of elements
    a = [float(x) for x in input().split()]
    b = [float(x) for x in input().split()]
    pi = [float(x) for x in input().split()]
    
    # Extract the dimensions of the transition matrix from the first two elements of the list
    transition_rows = int(a[0])
    transition_cols = int(a[1])
    
    # Create a zero transition matrix with rows by cols
    transition_matrix = [[0 for _ in range(transition_cols)] for _ in range(transition_rows)]
    
    # Extract the elements of the transition matrix from the remaining elements of the list
    for i in range(transition_rows):
        for j in range(transition_cols):
            transition_matrix[i][j] = float(a[2 + i * transition_cols + j])

    
    # Extract the dimensions of the emission matrix from the first two elements of the list
    emission_rows = int(b[0])
    emission_cols = int(b[1])
    
    # Create an emission matrix with the specified dimensions
    emission_matrix = [[0 for _ in range(emission_cols)] for _ in range(emission_rows)]
    
    # Extract the elements of the emission matrix from the remaining elements of the list
    for i in range(emission_rows):
        for j in range(emission_cols):
            emission_matrix[i][j] = float(b[2 + i * emission_cols + j])
    

    # Extract the dimensions of the initial state probability distribution matrix from the first two elements of the list
    initial_rows = int(pi[0])
    initial_cols = int(pi[1])
    
    # Create an initial state probability distribution matrix with the specified dimensions
    initial_matrix = [[0 for _ in range(initial_cols)] for _ in range(initial_rows)]
    # Extract the elements of the initial state probability distribution matrix from the remaining elements of the list
    for i in range(initial_rows):
        for j in range(initial_cols):
            initial_matrix[i][j] = float(pi[2 + i * initial_cols + j])
    
##################################################################################
# output a string that matches the Kattis output
    next_state_probability = [    [        sum(initial_matrix[0][j] * transition_matrix[j][i]
                for j in range(len(initial_matrix[0])))
            for i in range(len(transition_matrix[0]))
        ]
    ]
    
    emission_probability = []
    for i in range(len(emission_matrix[0])):
        prob = 0
        for j in range(len(next_state_probability[0])):
            prob += next_state_probability[0][j] * emission_matrix[j][i]
        emission_probability.append(prob)
    

    formatted_emission_probability = list([])
    for i in range(len(emission_probability)):
        formatted_emission_probability.append(float('{:.1f}'.format(emission_probability[i])))
    
    print(''.join(map(str,formatted_emission_probability)))

if __name__ == "__main__":
    main()