# enginery-qualification-calc

A small command-line calculator kept as the **synthetic qualification target** for Enginery's live harness qualification. Its issues are written for qualification runs; work done here demonstrates the factory's mechanics, not its usefulness on real projects.

The project uses only the Python standard library so that its tests run offline inside Enginery's isolated runner image.

## Usage

```sh
python3 -m calc "2 + 3 * 4"      # prints 14
python3 -m calc "(1 + 2) / 4"    # prints 0.75
```

Supported: integers and decimals, `+ - * /`, parentheses and unary minus, with the usual precedence. An invalid expression prints `error: <reason>` on stderr and exits with status 2.

## Tests

```sh
python3 -m unittest
```

## Branches

- `main` — the calculator.
- `qualify/omp` and `qualify/claude` — `main` plus the Enginery project policy (`.enginery/project.toml`) for one harness and the acceptance check for that harness's qualification issue. Qualification pull requests target these branches.
