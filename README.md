# Hypervolume Ratio Computation (HVR) for Pareto Fronts

## Overview

This project provides a method to compute the Ratio of the Hypervolume (HVR) for a list of Pareto fronts. 

## Features

- **Aggregation into Accumulated Pareto Front:** Combines all solutions into a single solution to form the accumulated Pareto front.
- **Nadir and Ideal Point Extraction:** Extracts critical points from the accumulated Pareto front for normalization.
- **Pareto Front Normalization:** Normalizes each Pareto front using the nadir and ideal points from the accumulated Pareto front.
- **HVR Calculation:** Computes the HVR for each Pareto front by dividing its hypervolume by the hypervolume of the accumulated Pareto front.

## Usage

### Dependencies

- Python
- pandas
- scikit-learn

### Running the Code

1. **Modify the File List:** Update the `file_list` variable with the names of the files containing the Pareto fronts you want to analyze.
2. **Execute the Code:** Run the main script to compute the HVR for each file.

### Example

```python
file_list = ['pareto_front1.csv', 'pareto_front2.csv']
# Run the main code to compute the HVR
```

## Output

The code computes and prints the HVR for each specified Pareto front, and optionally it can save the normalized data to a text file if needed.

## Contributing

Contributions are welcome! Feel free to fork this repository and submit pull requests.

## License

[Apache](LICENSE)

