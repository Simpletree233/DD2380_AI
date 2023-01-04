# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 21:14:01 2022

@author: simpletree
"""

#TODO: add dimension and space between the output elements

def matrix_mul(X,Y):
    '''
    X = [ [1,2],[3,4],[4,5] ]
    # 2x3 matrix
    Y = [ [1,2,3],[4,5,6] ]
    '''
    # resultant matrix
    result = [[0 for _ in range(len(A))] for _ in range(len(B[0]))]

    # iterating rows of X matrix
    for i in range( len(X) ):
       # iterating columns of Y matrix
       for j in range(len(Y[0])):
           # iterating rows of Y matrix
           for k in range(len(Y)):
               result[i][j] += X[i][k] * Y[k][j]
    return results

def ele_wise_product(a:list,b:list):
    '''
    a : list
    b : list
        1xn column
    Returns a lsit
    '''
    if not(len(a) == len(b)):
        print ("Two list length Not equal!")
    else:
        result = [0 for _ in range(a)]
        for i in range(len(a)):
            result[i] = a[i]*b[i]
        return result

def main():
    # Split the line into a list of elements
    a = [float(x) for x in input().split()]
    b = [float(x) for x in input().split()]
    pi = [float(x) for x in input().split()]
    seq = [float(x) for x in input().split()]
    
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
            
    # Extract the dimensions of the emission sequence matrix from the first two elements of the list
    obs_seq = seq
    obs_row = seq[0]
    observation = obs_seq.pop(0)

    
##################################################################################
 
    # initilize alpha  at PAGE 59
    #initialize a zero alpha list
    alpha = [0 for _ in range(len(seq)-1)]

    #the index for fisrt element is 0
    alpha[0] = ele_wise_product(initial_matrix,emission_matrix[:, int(observation[0])])
    
    for i in range(len(observaiton)-1):
        # alpha(t+1) = ele_wise_product((A*alpha(t)), b(Observation(t+1)))
        alpha[i+1] = ele_wise_product(matrix_mul(transition_matrix, alpha[i]) , emission_matrix[:, observation[i+1]])


    pSeq = 0
    for j in range(len(observation)):
        pSeq = pSeq + alpha[j]

    print(str(pSeq))
    #print(''.join(map(str,formatted_emission_probability)))

if __name__ == "__main__":
    main()