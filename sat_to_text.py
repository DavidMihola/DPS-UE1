import sys, exceptions

def printf(format, *args):
    sys.stdout.write(format % args)

def length(number):
  return len(str(number))

# the inverse function to encode
def decode(number):
  number = number - 1

  weeks = max_team - 1
  fields = max_team / 2
  slots = weeks * fields

  if (number < (max_vars / 2)):
    position = 1
    team_offset = 1
  else:
    position = 2
    team_offset = 2
    number = number - (max_vars / 2)

  (team_index, slot_index) = divmod(number, slots)
  (row_index, col_index) = divmod(slot_index, weeks)

  return (col_index + 1, row_index + 1, team_index + team_offset, position)

### MAIN PROGRAM STARTS HERE ###

args = sys.argv
f = file(args[1], 'r')

variables = []

for line in f:
  for word in line.split(' '):
    try:
      number = int(word)
      if (number != 0):
        variables.append(number)
    except exceptions.ValueError:
      pass

variables_to_teams = {}

for teams in range (2, 20):
  vars = teams * (teams - 1) * (teams - 1)
  variables_to_teams[vars] = teams

max_vars = len(variables)
max_team = variables_to_teams[max_vars]

teams = range(1, max_team + 1)
weeks = range(1, (max_team - 1) + 1)
fields = range(1, (max_team / 2) + 1)

cells = []

for field in fields:
  row = []
  for week in weeks:
    row.append((0,0))
  cells.append(row)

positive_variables = filter(lambda x:x>0, variables)

for (week, field, team, position) in map(decode, positive_variables):
#  (week, field, team, position) = decode(clause)
  (oldteam1, oldteam2) = cells[field-1][week-1]
  if (position == 1):
    cells[field-1][week-1] = (team, oldteam2)
  if (position == 2):
    cells[field-1][week-1] = (oldteam1, team)  

def printcells(cells):
  for row in cells:
    for (team1, team2) in row:
      #if (team1 != 0):
        printf('%i:%i\t', team1, team2)
    print 


printcells(cells)

