# ComputorV1

## About

The goal of this project is to write a program that solves polynomial equations of second or lower degree.

The program shows:
- The equation in its reduced form
- The degree of the equation
- Its solution(s) and the polarity of the discriminant where applicable

## Installation
To install the project, clone the repository and run the following command:

```bash
git clone https://github.com/kosyan62/computor.git
cd computor
pip install .
```
## Usage
python3 computor.py [-h] [-v] equation
### Arguments
- `-h`: Show help message and exit
- `-v`: Show verbose output (includes discriminant calculation)
- `-s`: Show solution steps
- `equation`: Polynomial equation in the format "aX^2 + bX + c = 0"

### Examples

Quadratic equation:
```bash
python3 computor.py -v "X^2 - 1X + 1 = 0"
Reduced form: 1 * X^2 - 1 * X^1 + 1 * X^0 = 0
Polynomial degree: 2
Discriminant: -3
Solutions count: 2
Solutions: x = 1/2 + sqrt(3)*I/2, x = 1/2 - sqrt(3)*I/2
```