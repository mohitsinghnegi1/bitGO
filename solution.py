from turtle import *
import turtle
import time
import math
import requests 
import json
from heapq import heappush, heappop

# Problem Statement: 

# Example Block :  Block 680000. Block is a set of transactions.

# Block 680000 → [A, B, C, D, E, F]  transactions.
# A-> { inp:[ B, C ] }
# Every transaction can have 1-n input txns from the same block or from a different block.


# A -> [Y] as an input.	
# Since Y is not in the same Block. Y will not be considered as a parents
# Ancestor count for A ->0
# B-> [C, X] as inputs. 	
# Since C is in the same block, 
# C will be considered as a valid parent.
# Now dive deep into C
# Inputs of C → [D, E] 
# Now check D is in the same block, if yes go check D inputs/parents
# Example: No of Ancestor D -> 0  (W,Y)
# Now check E is in the same block,  if yes go check E inputs/parents
# Example: No of Ancestor E -> 1 (F)  [F->U,I]
# No of Ancestor for C -> D + E + Ancestors of D + Ancestors of E ⇒ 3
# Now check X, X is not in the block, ignore the txn
# No of ancestors for B => C + No of ancestors of C  => 1 + 3 ⇒ 4

# Sort by ancestor count.
# A->0
# B->4
# C->3
# D->0
# E->1
# F->0
# Expected result is
# B->4
# C->3
# E->1
# A->0
# F->0
# D->0


blockId = 680000
transactionIdBytes = requests.get("https://blockstream.info/api/block-height/"+ str(blockId)).content
transactionId = transactionIdBytes.decode('utf-8')

transactions = set()
parTxns = {} # map of parent transactions

offset = 0
while(True):
  
  transactionData = requests.get("https://blockstream.info/api/block/"+transactionId+"/txs/"+str(offset)).content
  transactionData = json_response = json.loads(transactionData)
  if(transactionData==[]):
    print(offset)
    break

  for transactionObj in transactionData:
    transactions.add(transactionObj['txid'])
    
    parTxns[transactionObj['txid']] = []
    
    for vinObj in  transactionObj['vin']:
      parTxns[transactionObj['txid']].append(vinObj['txid'])
    
    # print(len(parTxns[transactionObj['txid']]))
  offset+=25
  
  if(offset==100):
    break

print(transactions)
print(parTxns)

# time coplexity: O(N)
# space complexity 2N

# transactions =  set(["A", "B", "C", "D", "E", "F"])

def findParTxn(txn):
  
  return parTxns.get(txn)

# tiem O(N)  space: O(N)
def constructMappingGraph(transactions):
  
  graph = {}
  
  for txn in transactions:
    # TODO : find parent transactions of this
    parentTxn = findParTxn(txn)
    graph[txn] = parentTxn

  return graph
  
  
graph  = constructMappingGraph(transactions)

# graph = {"A":["Y"],
#         "B":["C","X"], #  1 + 3
#         "C":["D","E"], # C -> 1 + 1 + 1 
#         "D":["W","Y"],
#         "E":["F"],
#         "F":["U","I"]
#         }

def dfs(ctxn,visited):
  
  if(ctxn not in transactions):
    return 0
    
  # if(ctxn in visited):
  #   return 0
  
  count = 0
  for ptxn in graph[ctxn]:
    
    if(ptxn in transactions):
      count+=1
      count+= dfs(ptxn,visited)
  
  
  visited[ctxn] = True
  
  return count
  
# nLogN
heap = [] # [(3,txn3),(2,txn1), (2,txn2),]

# Time complexity: O(NLogN) 
# Space Complexity: O(N)

for transaction in transactions:
  visited = {}
  ansisterCount = dfs(transaction,visited) # O(E+V)
  heappush(heap, (-ansisterCount,transaction)) # logN

# n LogN
while(heap):
  count, txn = heappop(heap)  # LogN
  print(str(txn)+" -> "+ str(-count))


  




































