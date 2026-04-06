
"""
Script para exercício 1: reconciliar duas listas de transações
"""

from datetime import datetime
import csv
from pathlib import Path
from pprint import pprint

def group_transactions(transactions):
    """
    Agrupa transações por chave (departamento, valor, beneficiário).
    Assim só precisamos comparar transações das duas listas com mesma chave.

    Retorna um dicionário:
    chave -> lista de transações

    Cada transação armazenada contém:
    (data_convertida, data_original, dept, valor, beneficiário, índice_original)
    """
    groups = {}
    
    for idx, row in enumerate(transactions):
        date_str, dept, value, beneficiary = row
        date = datetime.strptime(date_str, "%Y-%m-%d")
        
        key = (dept, value, beneficiary)
        transaction = (date, date_str, dept, value, beneficiary, idx)
        
        if key not in groups:
            groups[key] = []
        
        groups[key].append(transaction)
    
    return groups


def reconcile_accounts(transactions1, transactions2):
    """
    Realiza a conciliação entre duas listas de transações.

    Para cada transação, tenta encontrar uma correspondente na outra lista:
    - Mesmo departamento, valor e beneficiário
    - Data pode variar em até +/- 1 dia
    - Cada transação pode ser usada apenas uma vez

    Retorna duas listas com uma nova coluna:
    'FOUND' ou 'MISSING'
    """
    groups1 = group_transactions(transactions1)
    groups2 = group_transactions(transactions2)
    
    # Preparar resultado final (mesmo tamanho das listas originais)
    result1 = [None] * len(transactions1)
    result2 = [None] * len(transactions2)
    
    # Iterar por todas as chaves possíveis
    all_keys = set(groups1.keys()).union(set(groups2.keys()))
    
    for key in all_keys:
        #se key nao existir, retorna vazio para evitar erro 
        group1 = groups1.get(key, [])
        group2 = groups2.get(key, [])
        
        # Ordenar por data (primeira "coluna")
        group1.sort(key=lambda x: x[0])
        group2.sort(key=lambda x: x[0])
        
        used = [False] * len(group2)
        matches1 = [False] * len(group1)
        matches2 = [False] * len(group2)
        
        # Matching
        for i, tran1 in enumerate(group1):
            date1 = tran1[0]
            
            for j, tran2 in enumerate(group2):
                if used[j]:
                    continue
                
                date2 = tran2[0]
                
                if abs((date1 - date2).days) <= 1:
                    used[j] = True
                    matches1[i] = True
                    matches2[j] = True
                    break
        
        # Reconstruir resultado para lista 1
        for i, tran1 in enumerate(group1):
            #ignoramos data que construimos no formato datetime ao usar o "_"
            _, date_str, dept, value, beneficiary, original_idx = tran1
            status = "FOUND" if matches1[i] else "MISSING"
            
            result1[original_idx] = [
                date_str, dept, value, beneficiary, status
            ]
        
        # Reconstruir resultado para lista 2
        for j, tran2 in enumerate(group2):
            #ignoramos data que construimos no formato datetime ao usar o "_"
            _, date_str, dept, value, beneficiary, original_idx = tran2
            status = "FOUND" if matches2[j] else "MISSING"
            
            result2[original_idx] = [
                date_str, dept, value, beneficiary, status
            ]
    
    return result1, result2

#testando para exemplo do exercicio
if __name__ == "__main__":
    transactions1 = list(csv.reader(Path('transactions1.csv').open()))
    transactions2 = list(csv.reader(Path('transactions2.csv').open()))
    out1, out2 = reconcile_accounts(transactions1, transactions2)
    pprint(out1)
    pprint(out2)