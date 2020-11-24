#!/usr/bin/env python
# coding: utf-8

# In[151]:


import time
from threading import Thread
from math import floor


# In[152]:


def separa_doc(arr_data, num):    
    global cpf_qtd
    global cnpj_qtd
    
    for i in range(0, len(arr_data)):
        if len(arr_data[i]) > 9:
            digito_cnpj(arr_data[i])
            cnpj_qtd += 1
        else:
            digito_cpf(arr_data[i])
            cpf_qtd += 1

    
    global arr_ver
    arr_ver[num] = True


# In[153]:


def pega_dados(arq):
    with open(arq, 'r') as a:
        return [i.strip() for i in a.read().splitlines()]


# In[154]:


def digito_cpf(cpf):
    cpf = cpf
    cpf = [int(x) for x in str(cpf)]
    v1 = 0
    v2 = 0
    for i in range(len(cpf)):
        v1 = v1 + cpf[i] * (9 - (i % 10))
        v2 = v2 + cpf[i] + (9 - ((i + 1) % 10))
    
    v1 = (v1 % 11) % 10
    v2 = v2 + v1 * 9
    v2 = (v2 % 11) % 10
    
    return '{}{}'.format(v1, v2)


# In[155]:


def digito_cnpj(cnpj):
    cnpj = [int(x) for x in str(cnpj)]
    v1 = 0
    v2 = 0
    # Calcula o primeiro dígito de verificação.
    v1 = (5 * cnpj[0]) + (4 * cnpj[1]) + (3 * cnpj[2]) + (2 * cnpj[3])
    v1 += (9 * cnpj[4]) + (8 * cnpj[5])  + (7 * cnpj[6])  + (6 * cnpj[7])
    v1 += (5 * cnpj[8]) + (4 * cnpj[9]) + (3 * cnpj[10]) + (2 * cnpj[11])
    v1 = 11 - v1 % 11
    
    if v1 >= 10:
        v1 = 0
    
    v2 = (6 * cnpj[0]) + (5 * cnpj[1])  + (4 * cnpj[2])  + (3 * cnpj[3])
    v2 += (2 * cnpj[4]) + (9 * cnpj[5])  + (8 * cnpj[6])  + (7 * cnpj[7])
    v2 += (6 * cnpj[8]) + (5 * cnpj[9]) + (4 * cnpj[10]) + (3 * cnpj[11])
    v2 += 2 * v1
    v2 = 11 - v2 % 11
    
    if v2 >=  10:
        v2 = 0  

    return '{}{}'.format(v1, v2)


# In[156]:


arr_ver = [0, 0, 0, 0, 0, 0]
cpf_qtd = 0
cnpj_qtd = 0

def main():
    global arr_ver
    tempo_inicial = time.time()
    
    arr_df = pega_dados('BASE.txt')
    n = 6
    saida = floor(len(arr_df)/n)
    part = arr_df[0:saida]

    threads = []
    for i in range(0, n):
        part = arr_df[saida*i:(i + 1)*saida]
        threads.append(Thread(target=separa_doc, args=(part, i,), daemon=True))
    
    for i in range(0, n):
        threads[i].start()
        arr_ver[i] = False
    
    
    while(True):
        flag = True
        for i in range(0, n):
            if arr_ver[i] == False:
                flag = False
            else:
                threads[i].join()
        
        if flag:
            break
    
    print('O total de documentos avaliados foi de', cpf_qtd + cnpj_qtd, 'documentos')
    print('Levando', (time.time() - tempo_inicial) * 1000, 'milisegundos')
    
    


# In[157]:


if __name__ == "__main__":
    main()

