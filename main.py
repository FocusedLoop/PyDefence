from my_seed import world
from render import render

w = world(xy=[100, 100], spread=3)
w.generate()

r = render(mode="terminal")
r.mode(r, w.map)