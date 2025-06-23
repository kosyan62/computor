# ComputorV1

## About

The goal of this project is to write a program that solves polynomial equations of second or lower degree.

The program shows:
- The equation in its reduced form
- The degree of the equation
- Its solution(s) and the polarity of the discriminant where applicable

## Installation
### Requirements
- Python 3.10 or higher
- Git

### Steps
1. Clone the repository:
```bash
git clone https://github.com/kosyan62/computor.git && cd computor
```
2. Create and activate a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install the required packages:

```bash
pip install .
```

## Usage
ft_computor_v1 [-h] [-v] equation
### Arguments
- `-h`: Show help message and exit
- `-v`: Show verbose output (includes discriminant calculation)
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
### Features
- Solves polynomial equations up to degree 2
- Supports real and complex number solutions
- Step-by-step solution display option
- Handles equations in standard mathematical notation

### Limitations
- Maximum coefficient value: ±1e308 (Python's float limits)
- Coefficients must be real numbers

### Troubleshooting
If you encounter issues:
1. Ensure your equation follows the correct format
2. Check that Python 3.10+ is installed
 
### Testing
To run the tests, use:
```bash
python3 -m pytest tests/
```