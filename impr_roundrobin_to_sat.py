import itertools, sys
from roundrobin_to_sat import *

args = sys.argv
max_team = int(args[1])
#print max_team
teams = range(1, max_team + 1)
weeks = range(1, max_team)
fields = range(1, (max_team / 2) + 1)
positions = range(1, 3)

max_vars = pow(10, 3 * length(max_team) + 1)

def improvementClauses():
  clauses = []
  for field in fields:
#    print field
    var1 = encode(1, field, 2*field - 1, 1)
    var2 = encode(1, field, 2*field, 2)
    clauses.append("{0} 0".format(var1))
    clauses.append("{0} 0".format(var2))
  return clauses

def improvementClauses2():
  clauses = []
  for week in weeks:
    vars = []
    for field in fields:
      vars.append(encode(week, field, week + 1, 2))
    clauses.append(" ".join(map(str, vars)) + " 0")
  return clauses

clauses = improvementClauses() + point2clauses() + point3clauses() + point4clauses() + point5clauses() + point6clauses()

print "p cnf", max_vars, len(clauses)

for clause in clauses:
  print clause



