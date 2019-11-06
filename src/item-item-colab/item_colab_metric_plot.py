import json
import item_colab_filtering
import matplotlib.pyplot as plt

K = [20, 30, 40, 50, 60, 70, 80, 90, 100]
tags = ['15-15','14-15', '13-15', '12-15', '11-15']

#generates 15-15 data plots, values ((mae, rmse, time) vs K)
with open("../../data/test_dataset15-15.json", "r") as read_file:
    test_dataset = json.load(read_file)
item_colab_filtering.plot_error_K(test_dataset, '15-15',  K)

#compare over datasets - scaling
mae = []
rmse = []
times = []
sizes = []
for tag in tags:
    with open("../../data/test_dataset"+ tag +".json", "r") as read_file:
        test_dataset = json.load(read_file)
    print(" ==== METRIC COMPUTE for %s ====" % tag)
    sizes.append(len(test_dataset))
    mae_values, rmse_values, t_values_error = item_colab_filtering.get_errors_time(test_dataset, tag, 60)
    mae.append(mae_values)
    rmse.append(rmse_values)
    times.append(t_values_error)

#plots
f1 = plt.figure(1)
print("SIZES AND MAE", sizes, mae)
plt.plot(sizes, mae, label = 'Item-based mae')
plt.legend()
plt.title("MAE vs Subset Size")
plt.xlabel("Subset Size")
plt.ylabel("MAE")
plt.savefig('../../output/item-item/mae_values.png')

f2 = plt.figure(2)
print("SIZES AND RMSE", sizes, rmse)
plt.plot(sizes, rmse, label = 'Item-based rmse')
plt.legend()
plt.title("RMSE vs Subset Size")
plt.xlabel("Subset Size")
plt.ylabel("RMSE")
plt.savefig('../../output/item-item/rmse_values.png')
f3 = plt.figure(3)

print("SIZES and TIMES ARE:", sizes, times)
plt.plot(sizes, times)
plt.title("Time vs Subset Size")
plt.xlabel("Subset Size")
plt.ylabel("Time (seconds)")
plt.savefig('../../output/item-item/time_values.png')
plt.show()