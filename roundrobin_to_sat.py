import itertools, sys
from sets import Set

### FUNCTION DEFINITIONS ###

def length(number):
  return len(str(number))

# encodes a combination of week, field, team, slot and position
# to a decimal number
# POST:	the length of the returned number must be a multiple of 3 plus 1,
#       i.e. week, field and team must always use the same number of digits
#       otherwise, decoding is not possible
# output format is: position(1 digit), week (x digits), field (x digits), team (x digits)
def encode(week, field, team, position):
  # the game-slots are numbered from the top left:
  # 1, 2, 3, ... weeks
  # weeks+1, weeks+2, ... 2*weeks
  #  ....................fields*weeks
  # so, there are:
  week_count = len(weeks)
  field_count = len(fields)
  slot_count = week_count * field_count

  if (position == 1):
    if ( (team < 1) or (team > max_team - 1) ):
#      print "Wrong team index!!! Team {0} can't be at position 1".format(team)
      return -1
    team_index = team - 1 #team 1 is 0, etc.
  else:
    if ( (team < 2) or (team > max_team) ):
#      print "Wrong team index!!! Team {0} can't be at position 2".format(team)
      return -1
    team_index = team - 2 #no team1, team2 is 0, etc.

  week_index = week - 1
  field_index = field - 1
  slot_index = field_index * week_count + week_index # going from 0*weeks + 0 up 

  slot_team = team_index * slot_count + slot_index

  # the first half is for teams in position 1
  # the second half is for teams in position 2
  return ( (max_vars / 2) * (position - 1) ) + slot_team + 1

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


  shift = pow(10, digits_per_field)
  tmp, team = divmod(number, shift)
  tmp, field = divmod(tmp, shift)
  position, week = divmod(tmp, shift)
  
  return (week, field, team, position)

def point2clauses():
  clauses = []
  for (week, field) in itertools.product(weeks, fields):
    vars1 = (encode(week, field, team, 1) for team in range (1, max_team))
    clauses.append(" ".join(map(str, vars1)) + " 0")
    vars2 = (encode(week, field, team, 2) for team in range (2, max_team + 1))
    clauses.append(" ".join(map(str, vars2)) + " 0")
  #print "2: ", len(clauses)
  return clauses

def point3clauses():
  clauses = []
#  for (week, field, team1) in itertools.product(weeks, fields, teams):
#    for team2 in range(1, team1 + 1):
  for (week, field, team1, team2) in itertools.product(weeks, fields, teams, teams):
    if (team1 >= team2):
      var1 = encode(week, field, team1, 1)
      var2 = encode(week, field, team2, 2)
#      print "Next clause:"
#      print week, field, team1, 1
#      print week, field, team2, 2
      if (var1 != -1) and (var2 != -1):
        clauses.append("-{0} -{1} 0".format(var1, var2))
  #print "3: ", len(clauses)
  return clauses

def point4clauses():
  clauses = []
  for (week, team, field1, field2, r1, r2) in itertools.product(weeks, teams, fields, fields, positions, positions):
    # the first team (number 1) can never play in the second position of( a slot:
    if ( (team == 1) and ((r1 == 2) or (r2 == 2)) ): continue
    # also, the last team (number max_team) can never play in the first position of a slot:
    if ( (team == max_team) and ((r1 == 1) or (r2 == 1)) ): continue
  
    var1 = encode(week, field1, team, r1)
    var2 = encode(week, field2, team, r2)

    if (var1 != var2) and (var1 != -1) and (var2 != -1):
      clauses.append("-{0} -{1} 0".format(var1, var2))
  #print "4: ", len(clauses)
  return clauses

def point5clauses():
  clauses = []
  for (week1, week2, field1, field2, team1) in itertools.product(weeks, weeks, fields, fields, teams):
    if (week1 != week2):
      for team2 in range(team1 + 1, max_team + 1):
        var1 = encode(week1, field1, team1, 1)
        var2 = encode(week1, field1, team2, 2)
        var3 = encode(week2, field2, team1, 1)
        var4 = encode(week2, field2, team2, 2)
        if (var1 != -1) and (var2 != -1) and (var3 != -1) and (var4 != -1):
          clauses.append("-{0} -{1} -{2} -{3} 0".format(var1, var2, var3, var4))
  #print "5: ", len(clauses)
  return clauses

def point6clauses():
  clauses = []
  for (team, field, week1, r1, r2, r3) in itertools.product(teams, fields, weeks, positions, positions, positions):
    for week2 in range(week1 + 1, max_team):
      for week3 in range(week2 + 1, max_team):
        var1 = encode(week1, field, team, r1)
        var2 = encode(week2, field, team, r2)
        var3 = encode(week3, field, team, r3)
        if (var1 != -1) and (var2 != -1) and (var3 != -1):
          clauses.append("-{0} -{1} -{2} 0".format(var1, var2, var3))
  #print "6: ", len(clauses)
  return clauses


### MAIN PROGRAM STARTS HERE ###

args = sys.argv
max_team = int(args[1])
#print max_team
teams = range(1, max_team + 1)
position1teams = range(1, max_team)
position2teams = range(2, max_team + 1)
weeks = range(1, max_team)
fields = range(1, (max_team / 2) + 1)
positions = range(1, 3)

max_vars = max_team * (max_team -1) * (max_team -1)

def main():

  '''
  vars = Set([])
  errs = 0

  for (week, field, team, position) in itertools.product(weeks, fields, position1teams, [1]):
    var = encode(week, field, team, position)
    if (var in vars):
      print "Fehler: ", var,
      print "codiert aus ({}, {}, {}, {})".format(week, field, team, position)
      errs += 1
    else:
      print "OK: ", var,
      print "codiert aus ({}, {}, {}, {})".format(week, field, team, position)
      vars.add(var)

  
  for (week, field, team, position) in itertools.product(weeks, fields, position2teams, [2]):
    var = encode(week, field, team, position)
    if (var in vars):
      print "Fehler: ", var,
      print "codiert aus ({}, {}, {}, {})".format(week, field, team, position)
      errs += 1
    else:
      print "OK: ", var,
      print "codiert aus ({}, {}, {}, {})".format(week, field, team, position)
      vars.add(var)
  


  print "{0} Fehler".format(errs)
  print "Set enthaelt {0} Variablen".format(len(vars))

  print(list(vars))
  '''


  clauses = point2clauses() + point3clauses() + point4clauses() + point5clauses() + point6clauses()

  print "p cnf", max_vars, len(clauses)

  for clause in clauses:
    print clause
  
if __name__ == "__main__":
    main()



