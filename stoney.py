# Imports
import os, logging, datetime, random
import pandas as pd
import numpy as np
import tkinter as tk
from faker import Faker
from tkinter import filedialog, simpledialog, messagebox

# Initializations
#Logging
logging.basicConfig(
    level=logging.INFO,
    filemode='a',
    filename='log.txt',
    format='%(levelname)s - %(message)s'
)

#TKinter
root = tk.Tk()
root.withdraw()

#Faker
fake = Faker()

#Random seed
np.random.seed(42)
random.seed(42)

# Paths
folder_path = r'./'
file_path = os.path.join(folder_path, 'csv')
csv_path = os.path.join(file_path, 'lab.csv')

#Create paths
if not os.path.exists[file_path, folder_path]:
    os.mkdir[file_path, folder_path]
    logging.info("Creating directories...")
logging.info("Directories exist...")
if not os.path.exists(csv_path):
    pd.DataFrame.to_csv(csv_path, index=False)

# Helper Functions
#Save CSV
def saveCsv(data, path):
    df = pd.DataFrame([data])
    df.to_csv(path, index=False)
#Close
def close():
    cancel = messagebox.askyesnocancel