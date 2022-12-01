
#import None


A=[[0.2, 0.5, 0.3 ,0.0], 
[0.1, 0.4, 0.4, 0.1] ,
[0.2, 0.0, 0.4, 0.4],
[0.2 ,0.3, 0.0 ,0.5]]

B = [[1.0, 0.0, 0.0, 0.0], 
[1.0 ,0.0, 0.0 ,0.0 ],
[1.0, 0.2, 0.6 ,0.2]]

#A = list[][]  # 4x4   
#B =list[][]   # 4x3  emisision matrix
pi=[0.0, 0.0, 0.0, 1.0]   # 1x4

#   * is matric multiply operand

#pi * (A)^4 * B 

#for i in range(len(pi)):
    

#result = MM(pi,A)


"""
def matirx_multipy(A:list, B:list):
    if not len(A)[1] == len(B)[0]:
        return ('Couldnt be multiplied')
    else:
        temp = list(3,3)
"""       



def MM(a,b):
    c = []
    for i in range(0,len(a)):
        temp=[]
        for j in range(0,len(b[0])):
            s = 0
            for k in range(0,len(a[0])):
                s += a[i][k]*b[k][j]
            temp.append(s)
        c.append(temp)

    return c


