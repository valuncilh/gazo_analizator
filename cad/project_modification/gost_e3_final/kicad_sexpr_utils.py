#!/usr/bin/env python3
"""Minimal KiCad S-expression helpers used by the independent wired layout generator."""
import re, uuid

class Q(str): pass

def parse_sexpr(text):
    token_re = re.compile(r'\s*(;[^\n]*|"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+)')
    tokens=[]
    for m in token_re.finditer(text):
        t=m.group(1)
        if not t.startswith(';'):
            tokens.append(t)
    pos=0
    def parse_one():
        nonlocal pos
        if tokens[pos]=='(':
            pos+=1; arr=[]
            while pos < len(tokens) and tokens[pos] != ')':
                arr.append(parse_one())
            if pos >= len(tokens): raise ValueError('Unclosed S-expression')
            pos+=1
            return arr
        t=tokens[pos]; pos+=1
        if t.startswith('"'):
            return Q(t[1:-1])
        return t
    root=parse_one()
    if pos != len(tokens): raise ValueError('Unexpected tokens after root')
    return root

def dump_sexpr(node, level=0):
    ind='\t'*level
    if not isinstance(node,list):
        if isinstance(node,Q): return '"'+str(node)+'"'
        return str(node)
    if not node: return '()'
    # keep compact scalar lists for coordinates, version, etc.
    if all(not isinstance(x,list) for x in node):
        return '('+' '.join(dump_sexpr(x,level+1) for x in node)+')'
    parts=['(' + dump_sexpr(node[0], level+1)]
    for child in node[1:]:
        if isinstance(child,list):
            parts.append('\n'+'\t'*(level+1)+dump_sexpr(child,level+1))
        else:
            parts[-1] += ' ' + dump_sexpr(child,level+1)
    return ''.join(parts)+')'

def head(x): return x[0] if isinstance(x,list) and x else None
def kids(x,k): return [a for a in x if head(a)==k]
def one(x,k):
    a=kids(x,k)
    return a[0] if a else None
def qstr(x): return str(x) if x is not None else ''
def fnum(x): return float(x)
def fmt(v):
    if abs(v)<1e-8: v=0.0
    return f'{v:.4f}'.rstrip('0').rstrip('.')
def new_uuid(): return str(uuid.uuid4())
def replace_at(node, x, y, angle=None):
    at=one(node,'at')
    if at:
        at[1]=fmt(x); at[2]=fmt(y)
        if angle is not None and len(at)>3: at[3]=fmt(angle)

def descendants(node, key):
    out=[]
    if isinstance(node,list):
        if head(node)==key: out.append(node)
        else:
            for c in node: out.extend(descendants(c,key))
    return out

