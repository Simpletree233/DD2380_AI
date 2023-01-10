def viterbi(transition_matrix, emission_matrix, initial_matrix, observation):
    num_states = len(transition_matrix)
    num_emiss = len(new_obs)

    viterbi = [[0 for x in range(num_states)] for y in range(num_emiss)]
    path = [[0 for x in range(num_states)] for y in range(num_emiss-1)]
    
    for i in range(num_states):
            viterbi[0][i] = initial_matrix[0][i]*emission_matrix[i][new_obs[0]]
        
    for t in range(1, num_emiss):
        for i in range(num_states):
            temp = []
            for j in range(num_states):
                temp.append(viterbi[t-1][j]*transition_matrix[j][i]*emission_matrix[i][new_obs[t]])
            max_value = max(temp)
            viterbi[t][i] = max_value
            path[t-1][i] = temp.index(max_value)

    result = []
    back_track = viterbi[num_emiss-1].index(max(viterbi[num_emiss-1]))
    result.append(back_track)
    for t in range(num_emiss-2, -1, -1):
        back_track = path[t][back_track]
        result.append(back_track)
    result.reverse()
    return result

a = [float(x) for x in input().split()]
b = [float(x) for x in input().split()]
pi = [float(x) for x in input().split()]
seq = [float(x) for x in input().split()]

# with open('hmm2_02.in', 'r') as file:
#     lines = file.readlines()

# a = [float(x) for x in lines[0].split()]
# b = [float(x) for x in lines[1].split()]
# pi = [float(x) for x in lines[2].split()]
# seq = [int(x) for x in lines[3].split()]



transition_rows = int(a[0])
transition_cols = int(a[1])
transition_matrix = [[0 for _ in range(transition_cols)] for _ in range(transition_rows)]

for i in range(transition_rows):
    for j in range(transition_cols):
        transition_matrix[i][j] = float(a[2 + i * transition_cols + j])


emission_rows = int(b[0])
emission_cols = int(b[1])
emission_matrix = [[0 for _ in range(emission_cols)] for _ in range(emission_rows)]

for i in range(emission_rows):
    for j in range(emission_cols):
        emission_matrix[i][j] = float(b[2 + i * emission_cols + j])


initial_rows = int(pi[0])
initial_cols = int(pi[1])
initial_matrix = [[0 for _ in range(initial_cols)] for _ in range(initial_rows)]

for i in range(initial_rows):
    for j in range(initial_cols):
        initial_matrix[i][j] = float(pi[2 + i * initial_cols + j])


obs_seq = seq
observation = obs_seq[1:]
new_obs = []
for o in observation:
    new_obs.append(int(o))


most_likely_seq = viterbi(transition_matrix, emission_matrix, initial_matrix, new_obs)
print(" ".join(str(x) for x in most_likely_seq))
