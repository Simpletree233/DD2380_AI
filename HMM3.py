import math

def forward():
    num_emis = len(new_obs)
    num_states = len(transition_matrix)
    alpha = [[0 for x in range(num_states)] for y in range(num_emis)]
    scale = [0 for x in range(num_emis)]

    for i in range(num_states):
        alpha[0][i] = initial_matrix[0][i]*emission_matrix[i][new_obs[0]]
        scale[0] += alpha[0][i]

    scale[0] = 1/scale[0]
    for i in range(num_states):
        alpha[0][i] = alpha[0][i]*scale[0]

    for t in range(1, num_emis):
        for i in range(num_states):
            for j in range(num_states):
                alpha[t][i] += alpha[t-1][j]*transition_matrix[j][i]
            alpha[t][i] = alpha[t][i]*emission_matrix[i][new_obs[t]]
            scale[t] += alpha[t][i]
        
        # scale alpha at time step t
        scale[t]=1/scale[t]
        for i in range(num_states):
            alpha[t][i] = scale[t]*alpha[t][i]

    return [alpha, scale]

def backward(scale):
    num_emis = len(new_obs)
    num_states = len(transition_matrix)
    beta = [[0 for x in range(num_states)] for y in range(num_emis)]

    for i in range(num_states):
        beta[num_emis-1][i] = scale[num_emis-1]
    

    for t in range(num_emis-2, -1, -1):
        for i in range(num_states):
            for j in range(num_states):
                beta[t][i] += transition_matrix[i][j]*emission_matrix[j][new_obs[t+1]]*beta[t+1][j]
            beta[t][i] *= scale[t]
    return beta



def gamma(alpha, beta):
    num_emis = len(new_obs)
    num_states = len(transition_matrix)
    gamma = [[0.0 for x in range(num_states)] for y in range(num_emis)] 
    di_gamma = [[[0.0 for x in range(num_states)] for y in range(num_states)] for z in range(num_emis)]
    for t in range(num_emis-1):
        for i in range(num_states):
            for j in range(num_states):
                di_gamma[t][i][j] = alpha[t][i]*transition_matrix[i][j]*emission_matrix[j][new_obs[t+1]]*beta[t+1][j]
                #updates the value of gamma for the current state i at time t by adding the probability of transitioning from the current state i to all other states j at time t+1.
                gamma[t][i] += di_gamma[t][i][j]

    for i in range(num_states):
        gamma[num_emis-1][i] = alpha[num_emis-1][i]
    
    return [gamma, di_gamma]


def estimate(gamma, di_gamma):
    num_emis = len(new_obs)
    num_states = len(transition_matrix)
    M = len(emission_matrix[0])

    for i in range(num_states):
        initial_matrix[0][i] = gamma[0][i]
    
    for i in range(num_states):
        denom = 0
        for t in range(num_emis-1):
            denom += gamma[t][i]
        for j in range(num_states):
            numer = 0
            for t in range(num_emis-1):
                numer += di_gamma[t][i][j]
            transition_matrix[i][j] = numer/denom
    
    for i in range(num_states):
        denom = 0
        for t in range(num_emis):
            denom += gamma[t][i]
        for j in range(M):
            numer = 0
            for t in range(num_emis):
                if new_obs[t] == j:
                    numer += gamma[t][i]
            emission_matrix[i][j] = numer/denom

def log_prob(scale):
    num_emis = len(new_obs)
    logProb = 0
    for t in range(num_emis):
        logProb += math.log(scale[t])
    logProb = -logProb
    return logProb


def baum_welch(max):
    old_log_prob = -math.inf
    
    for i in range(max):
        alpha, scale = forward()
        beta = backward(scale)
        gamma1, di_gamma = gamma(alpha, beta)
        estimate(gamma1, di_gamma)

        log_prob1 = log_prob(scale)
        if log_prob1 > old_log_prob:
            old_log_prob = log_prob1
        else:
            break

    print(str(len(transition_matrix)) + ' ' + str(len(transition_matrix[0])), end=' ')
    for i in transition_matrix:
        for j in i:
            print(round(j, 6), end=' ')

    print(str(len(emission_matrix)) + ' ' + str(len(emission_matrix[0])), end=' ')
    for i in emission_matrix:
        for j in i:
            print(round(j, 6), end=' ')
    



a = [float(x) for x in input().split()]
b = [float(x) for x in input().split()]
pi = [float(x) for x in input().split()]
seq = [float(x) for x in input().split()]

# with open('hmm2_03.in', 'r') as file:
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

most_likely_seq = baum_welch(100)