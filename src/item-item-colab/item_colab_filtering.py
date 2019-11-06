import time
import matplotlib.pyplot as plt
import json
import evaluation

def plot_error_K(test_dataset, tag, K):
    with open("../../data/id_to_user"+ tag +".json", "r") as read_file:
        id_to_user = json.load(read_file)
    with open("../../data/user_to_id"+ tag +".json", "r") as read_file:
        user_to_id = json.load(read_file)
    
    log_error = {}
    t_values_error = []
    mae_values = []
    rmse_values = []
    mae_baseline = [0.825 for i in range(len(K))]
    rmse_baseline = [0.902 for i in range(len(K))]
    
    for k in K:
        strt = time.time()
        mae, rmse = evaluation.get_errors(test_dataset, tag, k)
        end = time.time()
        log_error[k] = (mae, rmse, end-strt)
        mae_values.append(mae)
        rmse_values.append(rmse)
        t_values_error.append(end - strt)
    with open('error_values'+ tag +'.txt', 'w') as outfile:
        json.dump(log_error, outfile)
    f1 = plt.figure(1)
    plt.plot(K, mae_values, marker='o', markerfacecolor='blue', color='skyblue', linewidth=1, label = 'Item-Item MAE')
    plt.plot(K, mae_baseline, marker='s', color='red', linewidth=1, label = 'Baseline MAE') #baseline mae
    plt.legend()
    plt.title("MAE vs K")
    plt.xlabel("K values (KNN)")
    plt.ylabel("MAE")
    plt.savefig('../../output/mae_values'+ tag +'.png')
    
    f2 = plt.figure(2)
    plt.plot(K, rmse_values, marker='o', markerfacecolor='blue', color='skyblue', linewidth=1, label = 'Item-Item RMSE')
    plt.plot(K, rmse_baseline, marker='s', color='red', linewidth=1, label = 'Baseline RMSE') #baseline rmse
    plt.legend()
    plt.title("RMSE vs K")
    plt.xlabel("K values (KNN)")
    plt.ylabel("RMSE")
    plt.savefig('../../output/rmse_values'+ tag +'.png')
    
    f3 = plt.figure(3)
    plt.plot(K, t_values_error, marker='o', markerfacecolor='blue', color='skyblue', linewidth=1)
    plt.title("Time vs K")
    plt.xlabel("K values (KNN)")
    plt.ylabel("Time (seconds)")
    plt.savefig('../../output/time_values'+ tag +'.png')
    plt.show()
    
def get_errors_time(test_dataset, tag, k):
    with open("../../data/id_to_user"+ tag +".json", "r") as read_file:
        id_to_user = json.load(read_file)
    with open("../../data/user_to_id"+ tag +".json", "r") as read_file:
        user_to_id = json.load(read_file)
    log_error = {}
    t_values_error = 0
    strt = time.time()
    mae, rmse = evaluation.get_errors(test_dataset, tag, k)
    end = time.time()
    log_error[k] = (mae, rmse, end-strt)
    t_values_error = end - strt
    with open('../../data/error_values'+ tag +'.json', 'w') as outfile:
        json.dump(log_error,outfile)
    return mae, rmse, t_values_error