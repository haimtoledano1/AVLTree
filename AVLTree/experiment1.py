from AVLTree import AVLTree
import random
import pandas as pd

# Function to run the experiment based on the image instructions
def run_experiment():
    sizes = [111 * (2 ** i) for i in range(1, 11)]  # Sizes: 111 * 2^i, for i in 1 to 10
    results = {"Size": sizes, "Sorted": [], "Reversed": [], "Random": [], "Neighbor Swaps": []}

    for n in sizes:
        experiments = {
            "Sorted": list(range(n)),
            "Reversed": list(range(n, 0, -1))
        }

        # Calculate averages for random and neighbor swaps experiments
        random_promotes = []
        neighbor_swaps_promotes = []

        for _ in range(20):
            # Generate random array
            random_arr = random.sample(range(n * 10), n)
            neighbor_swaps_arr = list(range(n))
            for i in range(n - 1):
                if random.random() < 0.5:
                    neighbor_swaps_arr[i], neighbor_swaps_arr[i + 1] = neighbor_swaps_arr[i + 1], neighbor_swaps_arr[i]

            # Run random experiment
            tree = AVLTree()
            promotes = 0
            for key in random_arr:
                _, _, promote_count = tree.finger_insert(key, str(key))
                promotes += promote_count
            random_promotes.append(promotes)

            # Run neighbor swaps experiment
            tree = AVLTree()
            promotes = 0
            for key in neighbor_swaps_arr:
                _, _, promote_count = tree.finger_insert(key, str(key))
                promotes += promote_count
            neighbor_swaps_promotes.append(promotes)

        # Store average results for random and neighbor swaps
        experiments["Random"] = sum(random_promotes) // 20
        experiments["Neighbor Swaps"] = sum(neighbor_swaps_promotes) // 20

        for exp_name, arr in experiments.items():
            tree = AVLTree()
            promotes = 0

            # Insert elements using finger_insert and count promotes
            if isinstance(arr, list):
                for key in arr:
                    _, _, promote_count = tree.finger_insert(key, str(key))
                    promotes += promote_count
            else:
                promotes = arr

            # Store results for each type
            results[exp_name].append(promotes)

    # Convert results to DataFrame
    df = pd.DataFrame(results)
    return df

# Run the experiment and display results
df_results = run_experiment()
print(df_results.to_string(index=False))
