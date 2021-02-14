#%%
%%latex

# Chess AI

Possible Moves `M(S)` from State `S(t)` to State `S(t+1)`

## Network Architecture

### Evaluator

- `f(S) = v`
- types = 6 pieces * 2 players = 13
- 64-bit-board for every type = 64 * 12 = 768 inputs
- 1 output for score `-1` - `1`
- deep NN

### Search

- Monte Carlo Tree Search

    - each state `S(t+1)` is given a score by `f(S(t+1)) = v`
    - time spend to explore each state `S` is proportional to `v(i) / sum(v)`
    - recursively explore States until the time for a State is > Threshold
    - play move leading to `max(v)`
    
### Training

After each game a score `s` is given:

     0 for draw
    -1 for loose
     1 for win

The error of the NN is `(s - v)^2 * r^(m - n) `, where `r` is the time drop of
parameter and `m` the number of moves in a game.