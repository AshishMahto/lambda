#!/usr/bin/env python3

import sys
from typing import Tuple

sys.setrecursionlimit(3000)

# -----
# This section is just used to implement tail-recursion.
# You probably don't need to reverse this but you can try if you want ;p
class TR(Exception):
  SEEN = []
  def __init__(self, key, args, kwargs):
    self.key = key
    self.args = args
    self.kwargs = kwargs

# memo proc
def T(fn, name=''):
  def _fn(*args, **kwargs):
    key = id(_fn)
    if key in TR.SEEN:
      raise TR(key, args, kwargs)
    else:
      TR.SEEN.append(key)
      while True:
        try:
          val = fn(*args, **kwargs)
          TR.SEEN = TR.SEEN[:TR.SEEN.index(key)]
          return val
        except TR as e:
          if e.key != key:
            raise
          else:
            args = e.args
            kwargs = e.kwargs
          TR.SEEN = TR.SEEN[:TR.SEEN.index(key)+1]
  return _fn

# -----
# Sice machine:

apply=lambda f:lambda arg_ls, **kwargs:f(*arg_ls, **kwargs)

# list functions
head=apply(lambda hd, *_:hd)
tail=apply(lambda _, *tl:tl)

# pair functions
fst=apply(lambda _1, _:_1)
snd=apply(lambda _, _2:_2)


mkList=lambda *_:_

# () - Bool False
if1=lambda b, then, els:head(tail(
  mkList(
    *(((),) * (b == ())),
    els,
    then)
))()

def if2(b, then, els): return els() if b == () else then()

mkTuple=lambda _:(_,)

# tuples are Bool
len_to_depth=apply(lambda *b, tree=():if1(b, lambda:len_to_depth(tail(b), tree=mkTuple(tree)), lambda:tree))

rotateL=apply(lambda *ls:mkList(*tail(ls), head(ls)))

depth_to_church_numeral_unmemoized=lambda depth, x, fun:if1(depth, lambda:depth_to_church_numeral_unmemoized(head(depth), fun(x), fun), lambda:x)

depth_to_church_numeral=T(lambda depth, x, fun:if1(depth, lambda:depth_to_church_numeral(head(depth), fun(x), fun), lambda:x))

rotateR=apply(lambda *ls:depth_to_church_numeral(head(len_to_depth(ls)), ls, rotateL))

                                                                    # remove 2nd
depth_extend=apply(lambda *args: if1(tail(args), lambda:depth_extend(mkList(mkTuple(head(args)), *tail(tail(args)))), lambda:mkTuple(head(args))))

get_python_depth1=lambda dep: depth_to_church_numeral(dep, 0, lambda x: x + 1)

num=get_python_depth1

def ht(tree): return 0 if tree == () else max(map(ht, tree)) + 1

map_acc=lambda ls1, fun, ls2:if1(ls1, lambda:map_acc(tail(ls1), fun, mkList(*ls2, fun(head(ls1)))), lambda:ls2)

map1=lambda ls, fun: map_acc(ls, fun, ())

def map_ls(ls, f): return [f(i) for i in ls]


encrypt= \
  lambda flag, prog, box:(if1(
    fst(head(prog)),
    lambda:if1(
      fst(fst(head(prog))),
      lambda:(mkList(head(box), *tail(flag)), rotateL(prog), tail(box)),
      lambda:(flag, rotateL(prog), mkList(head(flag), *box))
    ),
    lambda:if1(
      fst(snd(head(prog))),
      lambda:if1(
        fst(fst(snd(head(prog)))),
        lambda:(depth_to_church_numeral_unmemoized(head(box), flag, rotateL), rotateL(prog), tail(box)),
        lambda:(depth_to_church_numeral_unmemoized(head(box), flag, rotateR), rotateL(prog), tail(box)),
      ),
      lambda:if1(
        fst(snd(snd(head(prog)))),
        lambda:if1(
          fst(fst(snd(snd(head(prog))))),
          lambda:(flag, depth_to_church_numeral_unmemoized(head(fst(fst(snd(snd(head(prog)))))), prog, rotateR), box),
          lambda:(flag, depth_to_church_numeral_unmemoized(head(snd(fst(snd(snd(head(prog)))))), prog, rotateL), box)
        ),
        lambda:if1(
          fst(snd(snd(snd(head(prog))))),
          lambda:if1(
            fst(fst(snd(snd(snd(head(prog)))))),
            lambda:(flag, rotateL(prog), mkList(head(fst(fst(snd(snd(snd(head(prog))))))), *box)),
            lambda:(flag, rotateL(prog), mkList(head(depth_to_church_numeral(head(snd(fst(snd(snd(snd(head(prog))))))), box, rotateL)), *box))
          ),
          lambda:if1(
            fst(snd(snd(snd(snd(head(prog)))))),
            lambda:if1(
              fst(fst(snd(snd(snd(snd(head(prog))))))),
              lambda:(flag,
                      if1(
                        head(box),
                        lambda:rotateL(prog),
                        lambda:rotateL(rotateL(prog))),
                      tail(box)),
              lambda:(flag,
                      depth_to_church_numeral_unmemoized(head(box), prog, rotateL),
                      tail(box))
            ),
            lambda:if1(
              fst(snd(snd(snd(snd(snd(head(prog))))))),
              lambda:if1(
                fst(fst(snd(snd(snd(snd(snd(head(prog)))))))),
                lambda:(flag,
                        rotateL(prog),
                        mkList(depth_to_church_numeral(head(box), head(tail(box)), mkTuple), *tail(tail(box)))),
                lambda:(flag,
                        rotateL(prog),
                        mkList(depth_to_church_numeral(head(box), head(tail(box)), head), *tail(tail(box))))
              ),
              lambda:()
            )
          )
        )
      )
    )
  ))

lines = []

def runStep(flag, prog, box):
  i, instr0 = head(prog)
  # def print(s, end="\n"):
  #   global lines
  #   return lines.append(s + end)

  print(f'[{i:03}] - ',end="")
  global labels
  def getLabel(): return labels[i] if i in labels else ''

  if instr0[0]:
    if instr0[0][0]:
      print(f'read from box of {chr(num(head(box)))}: {num(head(box))}' + getLabel())
      return (
        mkList(head(box), *tail(flag)),
        rotateL(prog),
        tail(box)
      )
    else:
      print(f'write to box of {chr(num(head(flag)))}: {num(head(flag))}' + getLabel())
      return (
        flag,
        rotateL(prog),
        mkList(head(flag), *box)
      )
  else:
    if instr0[1][0]:
      if instr0[1][0][0]:
        print(f'rotateL flag of {num(head(box))}' + getLabel())
        return (
          depth_to_church_numeral_unmemoized(head(box), flag, rotateL),
          rotateL(prog),
          tail(box)
        )
      else:
        print(f'rotateR flag of {num(head(box))}' + getLabel())
        return (
          depth_to_church_numeral_unmemoized(head(box), flag, rotateR),
          rotateL(prog),
          tail(box)
        )
    else:
      if instr0[1][1][0]:          # fst(snd(snd(instr0))):
        if instr0[1][1][0][0]: # fst(fst(snd(snd(instr0)))):
          print(f'jump literal back' + getLabel())
          return (
            flag,
            depth_to_church_numeral_unmemoized(instr0[1][1][0][0][0], prog, rotateR),  # head(fst(fst(snd(snd(instr0)))))
            box
          )
        else:
          print(f'jump literal frwd' + getLabel())
          return (
            flag,
            depth_to_church_numeral_unmemoized(instr0[1][1][0][1][0], prog, rotateL),  # head(snd(fst(snd(snd(instr0)))))
            box
          )
      else:
        if instr0[1][1][1][0]:          # fst(snd(snd(snd(instr0)))):
          if instr0[1][1][1][0][0]: # fst(fst(snd(snd(snd(instr0))))):
            print(f'write literal to box of {num(instr0[1][1][1][0][0][0]):04}' + getLabel())
            return (
              flag,
              rotateL(prog),
              mkList(instr0[1][1][1][0][0][0], *box) # head(fst(fst(snd(snd(snd(instr0))))))
            )
          else:
            print(f'push box from peek of {num(instr0[1][1][1][0][1][0]):04}' + getLabel())
            return (
              flag,
              rotateL(prog),
              mkList(head(depth_to_church_numeral(instr0[1][1][1][0][1][0], box, rotateL)), *box) # head(snd(fst(snd(snd(snd(instr0))))))
            )
        else:
          if instr0[1][1][1][1][0]:          # fst(snd(snd(snd(snd(instr0))))):
            if instr0[1][1][1][1][0][0]: # fst(fst(snd(snd(snd(snd(instr0)))))):
              print(f'skip if box false (= 0)' + getLabel())
              return (
                flag,
                if1(head(box), lambda: rotateL(prog), lambda: rotateL(rotateL(prog))),
                tail(box)
              )
            else:
              print(f'unconditional jump of {num(head(box))}' + getLabel())
              return (
                flag,
                depth_to_church_numeral_unmemoized(head(box), prog, rotateL),
                tail(box)
              )
          else:
            if instr0[1][1][1][1][1][0]:          # fst(snd(snd(snd(snd(snd(instr0)))))):
              if instr0[1][1][1][1][1][0][0]: # fst(fst(snd(snd(snd(snd(snd(instr0))))))):
                print(f'box[0] <- {num(head(tail(box)))} + {num(head(box))}' + getLabel())
                return (
                  flag,
                  rotateL(prog),
                  mkList(depth_to_church_numeral(head(box), head(tail(box)), mkTuple), *tail(tail(box)))
                )
              else:
                print(f'box[0] <- {num(head(tail(box)))} - {num(head(box))}' + getLabel())
                return (
                  flag,
                  rotateL(prog),
                  mkList(depth_to_church_numeral(head(box), head(tail(box)), head), *tail(tail(box)))
                )
            else:
              return ()


labels = {}
curLabel = 0
ln = 0

def labelRun(i, instr0):
  global labels, curLabel, ln
  if not instr0[0] and not instr0[1][0] and instr0[1][1][0]:
    if instr0[1][1][0][0]: labels[(i - num(instr0[1][1][0][0][0])) % ln] = f'# label{curLabel:02}'
    else:                  labels[(i + num(instr0[1][1][0][1][0])) % ln] = f'# label{curLabel:02}'
    curLabel = curLabel + 1

def read_prog(i, instr0):
  """
  :param i: instr index
  :param instr0: instr val
  :return:
  """
  print(f'[{i:03}] - ',end="")
  global labels
  def getLabel(): return labels[i] if i in labels else ''

  if instr0[0]:
    if instr0[0][0]:
      print(f'0: box read\t\t\t\t\t\t' + getLabel())
      return 0
    else:
      print(f'1: box write\t\t\t\t\t' + getLabel())
      return 1
  else:
    if instr0[1][0]:
      if instr0[1][0][0]:
        print(f'2: cur pointer left\t\t\t\t' + getLabel())
        return 2
      else:
        print(f'3: cur pointer rite\t\t\t\t' + getLabel())
        return 3
    else:
      if instr0[1][1][0]:          # fst(snd(snd(instr0))):
        if instr0[1][1][0][0]: # fst(fst(snd(snd(instr0)))):
          print(f'4: jump backward to  {labels[(i - num(instr0[1][1][0][0][0])) % ln][2:]}\t' + getLabel())
          return 4
        else:
          print(f'5: jump forward  to  {labels[(i + num(instr0[1][1][0][1][0])) % ln][2:]}\t' + getLabel())
          return 5
      else:
        if instr0[1][1][1][0]:          # fst(snd(snd(snd(instr0)))):
          if instr0[1][1][1][0][0]: # fst(fst(snd(snd(snd(instr0))))):
            print(f'6: write literal box of {num(instr0[1][1][1][0][0][0]):04}\t' + getLabel())
            return 6
          else:
            print(f'7: push box from peek = {num(instr0[1][1][1][0][1][0]):04}\t' + getLabel())
            return 7
        else:
          if instr0[1][1][1][1][0]:          # fst(snd(snd(snd(snd(instr0))))):
            if instr0[1][1][1][1][0][0]: # fst(fst(snd(snd(snd(snd(instr0)))))):
              print(f'8: jump if box false' + getLabel())
              return 8
            else:
              print(f'9: unconditional jump\t\t' + getLabel())
              return 9
          else:
            if instr0[1][1][1][1][1][0]:          # fst(snd(snd(snd(snd(snd(instr0)))))):
              if instr0[1][1][1][1][1][0][0]: # fst(fst(snd(snd(snd(snd(snd(instr0))))))):
                print(f'A: box <- b[1] + b[0]\t\t' + getLabel())
                return 10
              else:
                print(f'B: box <- b[1] - b[0]\t\t' + getLabel())
                return 11
            else:
              return -1


recStep=T(lambda flag, prog, box:if1(prog[0][1], lambda:recStep(*runStep(flag, prog, box)), lambda:flag))

checkFlag=lambda flag, prog:map1(
  recStep(
    ((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()), # 20
    prog,
    mkList(
      *map1(map1(flag, wrapper1), depth_extend),
      *((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()) # 16
    )
  ),
  get_python_depth1
)

def wrapper1(char): return ((),) * char

# -----

def load(cs, i=0):
  objs = []
  while True:
    if cs[i+1] == ')':
      return tuple(objs), i+1
    elif cs[i+1] == '(':
      obj, i = load(cs, i+1)
      objs.append(obj)
    elif cs[i+1] == ',':
      i += 1

# this is apparently "too nested" for the native python parser, so we need to use a custom parser
prog_string = open('./prog', 'r').read()
prog, _ = load(prog_string)

prog = list(enumerate(prog))

ln = len(prog)
for i, e in prog[:-1]: labelRun(i, e)

# print(*[read_prog(i, e) for i, e in prog[:-1]],end='\n',sep=",")

flag = input('flag plz: ').encode('ascii')

def debugger():
  """
  Commands:
  p[fpb]?     - print all, or print flag/instr/box
  until int   - take steps until program reaches just before instruction int
  set[fb] int - set the head of flag/box to be int
  int         - take int steps
  """
  def setFB(strInt, rest):
    ret = ()
    for _ in range(int(strInt)): ret = (ret,)
    return tuple([ret] + rest)

  states = [(((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()), # 20
    prog,
    mkList(
      *map1(map1(flag, wrapper1), depth_extend),
      *((), (), (), (), (), (), (), (), (), (), (), (), (), (), (), ()) # 16
    ))]

  def nextStep():
    nonlocal states
    return () if states[-1] == () else runStep(*states[-1])

  while True:
    inp = input('-----\n')
    if inp[0] == 'p':
      if len(inp) == 1:
        print([num(i) for i in states[-1][0]])
        read_prog(*states[-1][1][0])
        print([num(i) for i in states[-1][2]])
      elif inp[1] == 'f': print([num(i) for i in states[-1][0]])
      elif inp[1] == 'p': read_prog(*states[-1][1][0])
      elif inp[1] == 'b': print([num(i) for i in states[-1][2]])
    elif inp[:6] == 'until ':
      j = int(inp[6:])
      while states[-1][1][0][0] != j:
        states.append(nextStep())
    elif inp[:3] == 'set':
      (f, p, b) = states[-1]
      which, what = inp[3:].split()
      if which == 'f':
        _, *f_tl = f
        states.append((setFB(what, f_tl), p, b))
        print([num(i) for i in states[-1][0]])
      else:
        _, *b_tl = b
        states.append((f, p, setFB(what, b_tl)))
        print([num(i) for i in states[-1][2]])
    else:
      nt = int(inp)
      if nt >= 0:
        for _ in range(nt):
          states.append(nextStep())
      else:
        for _ in range(-nt): states.pop()


if input("debugger? [y/n] ")[0] == 'y': debugger()

print('checking...')

# --- takes 1-2 minutes to check flag
o: Tuple = checkFlag(flag, prog)
# ---

print(o)

output = bytes(o[:o.index(0)]).decode('ascii')
print(output)

if output == b'Correct!':
  print('Flag: %s' % flag)
