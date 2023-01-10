def viterbi(transition_matrix, emission_matrix, initial_matrix, observation, max_iter=100):
    num_states = len(transition_matrix)
    num_emiss = len(observation)
    print(num_states)

    viterbi = [[0 for j in range(num_emiss)] for i in range(num_states)]
    path = [[0 for j in range(num_emiss)] for i in range(num_states)]
   
    for i in range(num_states):
        viterbi[i][0] = initial_matrix[i] * emission_matrix[i][observation[i]]

    iterations = 0

    for t in range(1, num_emiss):
        for s in range(num_states):
            trans_prob = [transition_matrix[i][s] * viterbi[i][t-1] for i in range(num_states)]
            state = trans_prob.index(max(trans_prob))
            viterbi[s][t] = trans_prob[state] * emission_matrix[s][observation[t]]
            path[s][t] = state
            iterations += 1
            if iterations >= max_iter:
                break
        if iterations >= max_iter:
            break
    final_state = max(range(num_states), key=lambda i: viterbi[i][num_emiss-1])
    most_likely_seq = [final_state]
    for i in range(num_emiss-2, -1, -1):
        final_state = path[final_state][i]
        most_likely_seq.append(final_state)
    return most_likely_seq[::-1]


# Split the line into a list of elements
# a = [float(x) for x in input().splitlines()[0]]
# b = [float(x) for x in input().splitlines()[1]]
# pi = [float(x) for x in input().splitlines()[2]]
# seq = [float(x) for x in input().splitlines()[3]]

with open('hmm2_02.in', 'r') as file:
    lines = file.readlines()

# Extract the dimensions of the transition matrix from the first two elements of the list
a = [float(x) for x in lines[0].split()]
b = [float(x) for x in lines[1].split()]
pi = [float(x) for x in lines[2].split()]
seq = [int(x) for x in lines[3].split()]


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
# initial_matrix = [float(pi[2 + i]) for i in range(initial_rows)]
# Extract the elements of the initial state probability distribution matrix from the remaining elements of the list
for i in range(initial_rows):
    for j in range(initial_cols):
        initial_matrix[i][j] = float(pi[2 + i * initial_cols + j])

print(initial_matrix)
# Extract the dimensions of the emission sequence matrix from the first two elements of the list
# obs_seq = seq
# obs_row = seq[0]
# observation = obs_seq.pop(0)

obs_seq = seq
observation = obs_seq[1:]



print(observation)


most_likely_seq = viterbi(transition_matrix, emission_matrix, initial_matrix, observation)
print(" ".join(str(x) for x in most_likely_seq))
