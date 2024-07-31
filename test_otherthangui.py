import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Example biased nd arrays
data_above_1 = np.random.randn(10, 10) * 0.5 + 1.5  # Example data biased above 1
data_below_1 = np.random.randn(10, 10) * 0.5 + 0.5  # Example data biased below 1
data_mixed = np.random.randn(10, 10) * 2 + 1        # Example mixed data
two_data = np.ones((10,10))
two_data[::2][::2] = 1.5
# Function to normalize data keeping 1 fixed
def normalize_data(data):
    normalized_data = np.copy(data)
    
    # Check if all values are >= 1
    if np.all(data >= 1):
        # Normalize values greater than 1 to [1, 2]
        min_val = 1
        max_val = np.max(data)
        normalized_data = 1 + (data - min_val) / (max_val - min_val)

    # Check if all values are <= 1
    elif np.all(data <= 1):
        # Normalize values less than 1 to [0, 1]
        min_val = np.min(data)
        max_val = 1
        normalized_data = (data - min_val) / (max_val - min_val)
        
    else:
        # Normalize values less than 1 to [0, 1]
        mask_less_than_1 = data < 1
        if np.any(mask_less_than_1):
            min_val = np.min(data[mask_less_than_1])
            max_val = 1
            normalized_data[mask_less_than_1] = (data[mask_less_than_1] - min_val) / (max_val - min_val)

        # Normalize values greater than 1 to [1, 2]
        mask_greater_than_1 = data > 1
        if np.any(mask_greater_than_1):
            min_val = 1
            max_val = np.max(data[mask_greater_than_1])
            normalized_data[mask_greater_than_1] = 1 + (data[mask_greater_than_1] - min_val) / (max_val - min_val)

    return normalized_data

# Apply normalization
normalized_data_above_1 = normalize_data(data_above_1)
normalized_data_below_1 = normalize_data(data_below_1)
normalized_data_mixed = normalize_data(data_mixed)
normalized_data_two = normalize_data(two_data)
test = np.array([[1., 1., 2., 2., 2., 2., 2.],[2,2,2,1,1,1,2]])
# Define the custom colormap
cdict = {
    'red':   [(0.0, 0.0, 0.0),
              (0.5, 1.0, 1.0),
              (1.0, 1.0, 1.0)],

    'green': [(0.0, 0.0, 0.0),
              (0.5, 1.0, 1.0),
              (1.0, 0.0, 0.0)],

    'blue':  [(0.0, 1.0, 1.0),
              (0.5, 1.0, 1.0),
              (1.0, 0.0, 0.0)]
}

custom_cmap = LinearSegmentedColormap('CustomMap', cdict)
print(normalized_data_two)
# Plot data
fig, axes = plt.subplots(1, 4, figsize=(15, 5))

axes[0].imshow(normalized_data_above_1, cmap=custom_cmap, vmin=0, vmax=2)
axes[0].set_title('Data Biased Above 1')


axes[1].imshow(normalized_data_below_1, cmap=custom_cmap, vmin=0, vmax=2)
axes[1].set_title('Data Biased Below 1')


axes[2].imshow(normalized_data_mixed, cmap=custom_cmap, vmin=0, vmax=2)
axes[2].set_title('Mixed Data')

axes[3].imshow(test, cmap=custom_cmap, vmin=0, vmax=2)
axes[3].set_title('Two Data')


plt.show()
