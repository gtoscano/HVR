# Hypervolume Ratio Computation (HVR) for Pareto Fronts

## Overview

This project offers a method to compute the Ratio of the Hypervolume (HVR) for a list of Pareto fronts. It first creates an accumulated Pareto front by aggregating solutions from multiple executions. From this accumulated Pareto front, the nadir and ideal points are extracted, which are key for normalizing the solutions. The accumulated hypervolume is then computed.

For each provided Pareto front, the solutions are normalized using the nadir and ideal points, and the hypervolume is computed. The Ratio of the Hypervolume (HVR) is calculated by dividing the computed hypervolume by the accumulated hypervolume.

The HVR provides a value between 0 and 1, where values closer to one are preferred, offering an insightful measure for multi-objective optimization problems.
## Features
- **Accumulated Pareto Front Construction**: Aggregates solutions from all executions to form the accumulated Pareto front.
- **Nadir and Ideal Point Extraction**: Identifies critical reference points for normalization.
- **Hypervolume Computation**: Computes the hypervolume of the accumulated Pareto front.
- **Pareto Front Normalization**: Normalizes individual Pareto fronts using the nadir and ideal points.
- **HVR Calculation**: Calculates the HVR for each Pareto front by dividing its hypervolume by the accumulated hypervolume.

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

The HVR provides a valuable metric for evaluating the quality of solutions in multi-objective optimization. Values closer to 1 indicate better alignment with the accumulated Pareto front, reflecting higher quality solutions.

## Contributing

Contributions are welcome! Feel free to fork this repository and submit pull requests.

## License

[Apache](LICENSE)

