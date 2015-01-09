from mud.core.util import *
from mud.core import *
import random


predicates.register("entity", has("entity"))

def idle(e):
  if dictionary(e):
    if e.get("ap") == 0:
      return True
  return False

register("idle", has("idle"))


@construct
def living(d):
    hpmax = d['hpmax']
    if parse.dice.is_dice(d['hpmax']):
        hpmax = parse.dice.roll(d['hpmax'])
    d['hp'] = hpmax
    d['hpmax'] = hpmax
    return d

@construct
def inventory(d):
  return {"contents":[]}

@construct
def acting(d):
  d["ap"] = random.randint(20,50)
  return d




@action
@given(has("acting"), number)
def update(a, delta):
  ap = a['acting']['ap']
  ap -= delta
  if ap < 0: ap = 0
  a['acting']['ap'] = ap

@action
@given(a("wandering", "idle", "entity"), number)
def update(a, delta):
  loc = location(a)
  if has("room")(loc):
    dests = connected_rooms(loc)
    dest = random.choice(dests)
    if act("walk", a, dest):
      a['acting']['ap'] = 30 + random.randint(1, 20)


@action
@given("entity", "room")
def walk(a, b):
  loc = location(a)
  if act("move", a, b):
    if loc:
      exits = the(loc,"exits")
      exit = False
      for k in exits:
        if exits[k] == the(b, "id"):
          exit = k 
      act("leave", loc, a, exit)
    act("arrive", a, b)
    return True
  return False

@action
@given("room", "entity", string)
def leave(o, e, b):
  report_to(o, "{#bold}"+act("indefinate_name", e), "leaves to the", b+".{#reset}")

@action
@given("entity", "room")
def arrive(e, r):
  report_to(r,  "{#bold}"+act("indefinate_name", e), "walks in.{#reset}")


