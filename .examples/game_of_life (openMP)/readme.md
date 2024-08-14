# Overload function examples.

## This example shows how to use openMP with pybind.
- benchmark result (**with** openMP):

```bash
python3 benchmarck.py
>>> At grid size 100, avg execution is 0.119 ms / iterations. (Performed : 500 iterations).
>>> At grid size 200, avg execution is 0.176 ms / iterations. (Performed : 500 iterations).
>>> At grid size 300, avg execution is 0.182 ms / iterations. (Performed : 500 iterations).
>>> At grid size 400, avg execution is 0.244 ms / iterations. (Performed : 500 iterations).
>>> At grid size 500, avg execution is 0.618 ms / iterations. (Performed : 500 iterations).
>>> At grid size 600, avg execution is 0.496 ms / iterations. (Performed : 500 iterations).
>>> At grid size 700, avg execution is 0.814 ms / iterations. (Performed : 500 iterations).
>>> At grid size 800, avg execution is 1.015 ms / iterations. (Performed : 500 iterations).
>>> At grid size 900, avg execution is 1.088 ms / iterations. (Performed : 500 iterations).
>>> At grid size 1000, avg execution is 1.400 ms / iterations. (Performed : 500 iterations).
```

- benchmark result (**without** openMP):
```bash
python3 benchmarck.py
>>> At grid size 100, avg execution is 0.085 ms / iterations. (Performed : 500 iterations).
>>> At grid size 200, avg execution is 0.198 ms / iterations. (Performed : 500 iterations).
>>> At grid size 300, avg execution is 0.435 ms / iterations. (Performed : 500 iterations).
>>> At grid size 400, avg execution is 0.746 ms / iterations. (Performed : 500 iterations).
>>> At grid size 500, avg execution is 1.161 ms / iterations. (Performed : 500 iterations).
>>> At grid size 600, avg execution is 1.678 ms / iterations. (Performed : 500 iterations).
>>> At grid size 700, avg execution is 2.319 ms / iterations. (Performed : 500 iterations).
>>> At grid size 800, avg execution is 2.979 ms / iterations. (Performed : 500 iterations).
>>> At grid size 900, avg execution is 3.807 ms / iterations. (Performed : 500 iterations).
>>> At grid size 1000, avg execution is 4.769 ms / iterations. (Performed : 500 iterations).
```
