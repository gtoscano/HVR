import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import pandas as pd

def read_all_files(file_list, columns):
    all_data = []
    
    for file_path in file_list:
        # Read only the specified columns from the CSV file
        df = pd.read_csv(file_path, usecols=columns)
        all_data.append(df)
    
    return all_data



def update(num, data):
    ax.cla()
    scatter = ax.scatter(data[num]['yield_mz'], data[num]['yield_sb'], data[num]['yield_wh'], c='blue', marker='o')
    
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_zlim(z_min, z_max)
    
    ax.set_xlabel('Yield MZ')
    ax.set_ylabel('Yield SB')
    ax.set_zlabel('Yield WH')
    return scatter,

if __name__ == "__main__":
    # Get a list of dataframes
    file_list = ['finalresults-1.csv', 'finalresults-2.csv', 'finalresults-3.csv',
'finalresults-4.csv', 'finalresults-5.csv', 'finalresults-6.csv',
'finalresults-7.csv', 'finalresults-8.csv', 'finalresults-7.csv',
'finalresults-10.csv']
    all_data = read_all_files(file_list, ['yield_mz','yield_sb','yield_wh'])

    x_min = min(df['yield_mz'].min() for df in all_data)
    x_max = max(df['yield_mz'].max() for df in all_data)
    y_min = min(df['yield_sb'].min() for df in all_data)
    y_max = max(df['yield_sb'].max() for df in all_data)
    z_min = min(df['yield_wh'].min() for df in all_data)
    z_max = max(df['yield_wh'].max() for df in all_data)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #ani = FuncAnimation(fig, update, frames=range(len(all_data)), fargs=(all_data,))
    
    ani = FuncAnimation(fig, update, frames=range(len(all_data)), fargs=(all_data,), interval=100)
    
    # Save as MP4 file
    ani.save('animation.mp4', writer='ffmpeg', fps=30, dpi=300, bitrate=1800)
    plt.show()

