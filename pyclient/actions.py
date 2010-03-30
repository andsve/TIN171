""" List of possible actions, preconditions and effects. See http://www.catan.com/en/download/?Settlers_of_Catan_Turn_Overview.pdf.

Explanatory:
  Have(Lumber, 1) is true if player has >0 Lumber
  !Have(Road, 1) is true if player has 0 Roads
  

Action( Buy(Road))
  PRECONDITIONS: RolledDices(), !Locked(), Have(Lumber, 1), Have(Brick, 1), !Have(Road, 1)
  EFFECTS: Locked(), Spend(Lumber, 1), Spend(Brick, 1), Gain(Road, 1)

Action( Build(Road, x))
  PRECONDITIONS: Locked(), RolledDices(), Have(Road, 1), RoadAllowed(x)
  EFFECTS: !Locked(), Spend(Road, 1), RoadAt(x), !RoadAllowed(x), RoadAllowed(x.neighbours)

Action( RollDices())
  PRECONDITIONS: !Locked(), !RolledDices()
  EFFECTS: RolledDices()

Action( PlayDevCard(Knight, x))
  PRECONDITIONS: !Locked(), Have(Knight, 1), !RobberAt(x)
  EFFECTS: RobberAt(x), StealFrom(x.players), Locked(), Spend(Knight, 1), Gain(KnightPoint, 1)

Action( Steal(x))
  PRECONDITIONS: Locked(), StealFrom(x)
  EFFECTS: !Locked(), StealFrom(reset), Gain(Random, 1)

Action( PlayDevCard(RoadBuilding))
  PRECONDITIONS: !Locked(), Have(RoadBuilding, 1)
  EFFECTS: Locked(), Gain(Road, 2), Spend(RoadBuilding, 1)

Action( PlayDevCard(Monopoly, x))

Action( PlayDevCard(Resources, x, y))

Action( Buy(Settlement))

Action( Build(Settlement, x))

Action( Buy(City, x))

Action( Buy(DevCard))
  PRECONDITIONS: Rolled(), !Locked(), Have(Ore, 1), Have(Wool, 1), Have(Grain, 1)
  EFFECTS: Spend(Ore, 1), Spend(Wool, 1), Spend(Grain, 1), Gain(DevCard)

Action( Trade(Bank, x, y))
  PRECONDITIONS: Rolled(), !Locked(), Have(x, 4)
  EFFECTS: Spend(x, 4), Gain(y, 1)

Action( Trade(3For1, x, y))
  PRECONDITIONS: Rolled(), !Locked(), Harbor(3For1), Have(x, 3)
  EFFECTS: Spend(x, 3), Gain(y, 1)

Action( Trade(x, y))
  PRECONDITIONS: Rolled(), !Locked(), Harbor(x), Have(x, 2)
  EFFECTS: Spend(x, 2), Gain(y, 1)
