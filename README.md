# SimplexMethod
## Input format
```dtd
number_of_variables
c1 c2 ... cn - function coefficients
number_of_inequalities
a_{11} a_{12} ... a_{1n}
...
a_{m1} a_{m2} ... a_{mn}
b_0 ... b_m - right parts of inequalities
```
## Cases processed
This implementation searches for the maximum of a function over a given range of acceptable values, which is specified as a system
a11 * x11 + ... a1n * x1n <= b1
...
am1 * xm1 + ... amn * xmn <= bm
The program correctly handles the cases of the existence of a maximum, the unlimited range of permissible values
## Notation
| Basis | C base | x0     | ... | x_{n-1)     | B | reduced_cost |
|-------| ------ |--------|-----|-------------|---|---|
| Ai1   | 0      | a00    | ... | a0n         | b0 |   |
| Ai2   | 0      | a10    | ... | a1n         | b1 |   |
|...|
|       | delta  | delta0 | ... | delta_{n-1} | F |   |
|       | c      | c0     | ... | c_{n-1}     |   |   |

delta_j = c_j - (column(xij), C_base)
