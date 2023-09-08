import numpy as np
import pandas as pd

# Generate 10 sets of random numbers

if __name__ == "__main__":
    for i in range(1, 11):
        # Generate a 100x3 matrix of random numbers
        data = np.random.rand(100, 3)
        
        # Create a DataFrame from the random numbers
        df = pd.DataFrame(data, columns=['yield_mz', 'yield_sb', 'yield_wh'])
        
        # Save the DataFrame to a CSV file
        df.to_csv(f'finalresults-{i}.csv', index=False)
