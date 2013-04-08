import itertools, sys

def length(number):
  return len(str(number))

# encodes a combination of week, field, team, slot and position
# to a decimal number
# POST:	the length of the returned number must be a multiple of 3 plus 1,
#       i.e. week, field and team must always use the same number of digits
#       otherwise, decoding is not possible
# output format is: position(1 digit), week (x digits), field (x digits), team (x digits)
def encode(week, field, team, position):
  # first determine the number of digits necessary to encode week, field and team
  digits_per_field = max(map(length, [week, field, team]))
#  print digits_per_field
  shift = pow(10, digits_per_field)
  tmp = position * shift + week
  tmp = tmp * shift + field
  tmp = tmp * shift + team
#  print tmp
  return tmp

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
max_team = int(args[1])
#print max_team
teams = range(1, max_team + 1)
weeks = range(1, (max_team - 1) + 1)
fields = range(1, (max_team / 2) + 1)
positions = range(1, 3)

max_vars = pow(10, 3 * length(max_team) + 1)

#print max_vars

#print weeks
#print fields

# first, one run through to count the clauses:

clauses = 0

#print "c clauses from 2."

for (week, field) in itertools.product(weeks, fields):
  list1 = (encode(week, field, team, 1) for team in range (1, max_team))
  clauses += 1 #print " ".join(map(str, list1)), 0
  list2 = (encode(week, field, team, 2) for team in range (2, max_team + 1))
  clauses += 1 #print " ".join(map(str, list2)), 0

#print "c clauses from 3."

for (week, field) in itertools.product(weeks, fields):
  for (team1, team2) in itertools.product(teams, teams):
    if (team1 >= team2): clauses += 1 #print -encode(week, field, team1, 1), -encode(week, field, team2, 2), 0

#print "c clauses from 4."

for (week, team, field1, field2, r1, r2) in itertools.product(weeks, teams, fields, fields, positions, positions):
  # the first team (number 1) can never play in the second position of( a slot:
  if ( (team == 1) and ((r1 == 2) or (r2 == 2)) ): continue
  # also, the last team (number max_team) can never play in the first position of a slot:
  if ( (team == max_team) and ((r1 == 1) or (r2 == 1)) ): continue
  
  var1 = encode(week, field1, team, r1)
  var2 = encode(week, field2, team, r2)

  if (var1 != var2): clauses += 1 #print -var1, -var2, 0

#print "c clauses from 5"

for (week1, week2, field1, field2, team1, team2) in itertools.product(weeks, weeks, fields, fields, teams, teams):
  if ( (week1 != week2) and (team1 < team2) ):
    var1 = encode(week1, field1, team1, 1)
    var2 = encode(week1, field1, team2, 2)
    var3 = encode(week2, field2, team1, 1)
    var4 = encode(week2, field2, team2, 2)
    clauses += 1 #print -var1, -var2, -var2, -var4, 0

#print "c clauses from 6"

for (team, field, week1, week2, week3, r1, r2, r3) in itertools.product(teams, fields, weeks, weeks, weeks, positions, positions, positions):
  if (week1 == week2) or (week2 == week3) or (week3 == week1): continue
  var1 = encode(week1, field, team, r1)
  var2 = encode(week2, field, team, r2)
  var3 = encode(week3, field, team, r3)
  clauses += 1 #print -var1, -var2, -var3, 0

for (field, team1, team2) in itertools.product (fields, teams, teams):
  if (team1 != team2 - 1):
    var1 = encode(1, field, team1, 1)
    var2 = encode(1, field, team2, 2)
    clauses += 1 #print -var1, -var2, 0

for (week, field, team) in itertools.product(weeks, fields, teams):
  if (week != team - 1):
    var1 = encode(week, field, 1, 1)
    var2 = encode(week, field, team, 2)
    clauses += 1 #print -var1, -var2, 0



print "p cnf", max_vars, clauses

print "c clauses from 2."

for (week, field) in itertools.product(weeks, fields):
  list1 = (encode(week, field, team, 1) for team in range (1, max_team))
  print " ".join(map(str, list1)), 0
  list2 = (encode(week, field, team, 2) for team in range (2, max_team + 1))
  print " ".join(map(str, list2)), 0

print "c clauses from 3."

for (week, field) in itertools.product(weeks, fields):
  for (team1, team2) in itertools.product(teams, teams):
    if (team1 >= team2): print -encode(week, field, team1, 1), -encode(week, field, team2, 2), 0

print "c clauses from 4."

for (week, team, field1, field2, r1, r2) in itertools.product(weeks, teams, fields, fields, positions, positions):
  # the first team (number 1) can never play in the second position of( a slot:
  if ( (team == 1) and ((r1 == 2) or (r2 == 2)) ): continue
  # also, the last team (number max_team) can never play in the first position of a slot:
  if ( (team == max_team) and ((r1 == 1) or (r2 == 1)) ): continue
  
  var1 = encode(week, field1, team, r1)
  var2 = encode(week, field2, team, r2)

  if (var1 != var2): print -var1, -var2, 0

print "c clauses from 5"

for (week1, week2, field1, field2, team1, team2) in itertools.product(weeks, weeks, fields, fields, teams, teams):
  if ( (week1 != week2) and (team1 < team2) ):
    var1 = encode(week1, field1, team1, 1)
    var2 = encode(week1, field1, team2, 2)
    var3 = encode(week2, field2, team1, 1)
    var4 = encode(week2, field2, team2, 2)
    print -var1, -var2, -var3, -var4, 0

print "c clauses from 6"

for (team, field, week1, week2, week3, r1, r2, r3) in itertools.product(teams, fields, weeks, weeks, weeks, positions, positions, positions):
  if (week1 == week2) or (week2 == week3) or (week3 == week1): continue
  var1 = encode(week1, field, team, r1)
  var2 = encode(week2, field, team, r2)
  var3 = encode(week3, field, team, r3)
  print -var1, -var2, -var3, 0

### Now, the improvements:

for (field, team1, team2) in itertools.product (fields, teams, teams):
  if (team1 != team2 - 1):
    var1 = encode(1, field, team1, 1)
    var2 = encode(1, field, team2, 2)
    print -var1, -var2, 0

for (week, field, team) in itertools.product(weeks, fields, teams):
  if (week != team - 1):
    var1 = encode(week, field, 1, 1)
    var2 = encode(week, field, team, 2)
    print -var1, -var2, 0
