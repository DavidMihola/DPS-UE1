import sys, exceptions

def printf(format, *args):
    sys.stdout.write(format % args)

def length(number):
  return len(str(number))

# the inverse function to encode
def decode(number):
  digits_per_field, remainder = divmod(length(number), 3)
#  print digits_per_field
  if remainder != 1:
    print "Fehler"
    return

  shift = pow(10, digits_per_field)
  tmp, team = divmod(number, shift)
  tmp, field = divmod(tmp, shift)
  position, week = divmod(tmp, shift)
  
  return (week, field, team, position)


### MAIN PROGRAM STARTS HERE ###

args = sys.argv
f = file(args[1], 'r')

clauses = []

for line in f:#sys.stdin:
  for word in line.split(' '):
    try:
      number = int(word)
      if (number > 0):
#        print decode(number)
	clauses.append(decode(number))
    except exceptions.ValueError:
      pass

max_team = max(x[2] for x in clauses)
#print "Max team: ", max_team
teams = range(1, max_team + 1)
weeks = range(1, (max_team - 1) + 1)
fields = range(1, (max_team / 2) + 1)


# the last number is the highest
digits_per_field = length(max_team)

#print "Digits per field: ",digits_per_field

cells = []

for field in fields:
  row = []
  for week in weeks:
    row.append((0,0))
  cells.append(row)

#print cells

for (week, field, team, position) in clauses:
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
