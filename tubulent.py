i = 0
        k = 0
        j = i + 1
        maior = 0
        
        while j < len(A):
            if k % 2 != 0:
                if A[k] > A[k+1]:
                    j += 1
                    k += 1
                    if (j - i) > maior:
                        maior = j - i
                else:
                    i += 1
                    k = i
                    j = i + 1
            else:
                if A[k] < A[k+1]:
                    j += 1
                    k += 1
                    if (j - i) > maior:
                        maior = j - i
                else:
                    i += 1
                    k = i
                    j = i + 1
        #rep
        i = 0
        k = 0
        j = i + 1
        while j < len(A):
            if k % 2 == 0:
                if A[k] > A[k+1]:
                    j += 1
                    k += 1
                    if (j - i) > maior:
                        maior = j - i
                else:
                    i += 1
                    k = i
                    j = i + 1
            else:
                if A[k] < A[k+1]:
                    j += 1
                    k += 1
                    if (j - i) > maior:
                        maior = j - i
                else:
                    i += 1
                    k = i
                    j = i + 1
                    
        if maior > 0:
            return maior
        else:
            return 1
