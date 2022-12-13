    
    # By testing the .py code, just 
    
    
    
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
    
    
    
    
    next_state_probability = [    [        sum(initial_matrix[0][j] * transition_matrix[j][i]
                for j in range(len(initial_matrix[0])))
            for i in range(len(transition_matrix[0]))
        ]
    ]
    
    
    
    # Multiply the result by the emission matrix to get the emission
    # probability distribution after the next transition
    
    emission_probability = []
    for i in range(len(emission_matrix[0])):
        prob = 0
        for j in range(len(next_state_probability[0])):
            prob += next_state_probability[0][j] * emission_matrix[j][i]
        emission_probability.append(prob)
    
    # Print the result in the required matrix format
    # print("%d %d" % (len(emission_probability), len(emission_probability[0])))
    # print(" ".join(" ".join(str(x) for x in row) for row in emission_probability))
    # Print the dimensions of the emission_probability matrix
    # print("%d %d" % (len(emission_probability), len(emission_probability[0])))
    
    # Format the elements of the matrix to display only one decimal place
    #formatted_emission_probability = [['{:.1f}'.format(x) for x in row] for row in emission_probability]
    formatted_emission_probability = list([])
    for i in range(len(emission_probability)):
        formatted_emission_probability.append(float('{:.1f}'.format(emission_probability[i])))
    
    
    # Concatenate the elements of the formatted matrix into a single string, separated by spaces
    #emission_probability_str = " ".join(" ".join(str(x) for x in row) for row in formatted_emission_probability)
    
    # Concatenate the dimensions of the matrix and its elements into a single string, separated by spaces
    #output_str = str(len(emission_probability)) + " " + str(len(emission_probability[0])) + " " + emission_probability_str
    #print(formatted_emission_probability)
    
    print(''.join(map(str,formatted_emission_probability)))
    
if __name__ == "__main__":
    main()
    
