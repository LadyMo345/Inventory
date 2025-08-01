#Import Packages
import os, logging, random, csv
import pandas as pd 
import numpy as np
import tkinter as tk
from faker import Faker
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox, simpledialog, ttk

# Initialize logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Tkinter
root = tk.Tk()
top= tk.Toplevel(root)
root.withdraw()  

# Initialize Faker
fake = Faker()

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Paths
root_path = r'./'
csv_path = os.path.join(root_path, 'csv')
lab_path = os.path.join(csv_path, "Lab.csv")
user_path = os.path.join(csv_path, "user.csv")

current_user = None
is_master =False 

user_file = "user.csv"
entries ={}

# Registration  function for users 
def register_form (): 
    reg_frame =tk.Toplevel(root)
    reg_frame.title("Register New User")
    reg_frame.geometry("300x250")
    
    tk.Label(reg_frame, text="Username").pack()
    id_username_entry =tk.Entry(reg_frame)
    id_username_entry.pack()
    
    tk.Label(reg_frame, text="Password").pack()
    id_password_entry =tk.Entry(reg_frame)
    id_password_entry.pack()
    
    tk.Label(reg_frame, text="Confirm Password").pack()
    id_confirm_entry =tk.Entry(reg_frame)
    id_confirm_entry.pack()
    
    is_master_note =tk.BooleanVar()
    
    is_master_noted_checkbox =tk.Checkbutton(reg_frame, text ="Register as master user", variable =is_master_note)
    is_master_noted_checkbox.pack()
    
    def Detail_submit(): 

        is_master_flag= is_master_note.get().strip()
        username =id_username_entry.get().strip()
        password =id_password_entry.get().strip()
        confirm_password =id_confirm_entry.get()
    
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "All fields are required")
            return 
        if password !=confirm_password:
            messagebox.showerror("Error", "Passwords does not match.")
            return
        if len(password)< 6: 
            messagebox.showwarning("Weak Password", "Password should be atleast 6 characters.")
            return
        for user in upload_users(): 
            if user['username']==username: 
                messagebox
#Check if user already exist
        if os.path.exists(user_file): 
            with open (user_file, newline ='') as f: 
                reader =csv.DictReader(f)
                for row in reader:
                    if row['username '] == username:
                        messagebox.showerror("Error", "Username already exists. ")
                        return
    
#Save  registration to file
        with open(user_file, "a", newline ='') as f: 
            writer =csv.writer(f)
            if os.stat(user_file).st_size == 0:
                writer.writerow(["userame", "password", "is_master"])
            writer.writerow([username, password, str(is_master_flag)])
            
        messagebox.showinfo("Success", "User registered Successfully.")
        reg_frame.destroy()
    tk.Button(reg_frame, text ="Register", command= Detail_submit).pack( pady=10) 
def upload_users(): 
    users =[]
    if os.path.exists(user_file): 
        with open(user_file, newline='')as f: 
            reader =csv.DictReader(f)
            users =list(reader)
            
    return users
def login_user(): 
    login_win =tk.Toplevel(root)    
    login_win.title("Login")
    login_win.geometry("300x200")
    
    tk.Label(login_win, text="Username").pack()
    user_entry = tk.Entry(login_win)
    user_entry.pack()

    tk.Label(login_win, text="Password").pack()
    pass_entry = tk.Entry(login_win, show="*")
    pass_entry.pack()

    def attempt_login():
        global current_user, is_master
        username = user_entry.get().strip()
        password = pass_entry.get().strip()
        if os.path.exists(user_file):
            with open(user_file, newline='') as f:
                for row in csv.DictReader(f):
                    if row["username"] == username and row["password"] == password:
                        current_user = username
                        is_master = row["is_master"].lower() == "true"
                        messagebox.showinfo("Login Success", f"Welcome {username}")
                        login_win.destroy()
                        open_inventory_menu()
                        return
        messagebox.showerror("Error", "Invalid credentials")

    tk.Button(login_win, text="Login", command=attempt_login).pack(pady=10)
    
def open_inventory_menu():
    main_menu_frame.pack()
    welcome_label.config(text=f"Logged in as: {current_user} ({'Master' if is_master else 'User'})")
    
def logout():
    global current_user, is_master
    current_user = None
    is_master = False
    main_menu_frame.pack_forget()
    messagebox.showinfo("Logout", "You have been logged out.")
    
def login_window():
    global current_user 
    username = simpledialog.askstring("Login", "Enter your username:")
    password = simpledialog.askstring("Login", "Enter your password:", show ="*")
    
    if validate_user(username, password):
        current_user =username 
        logging.info(f"logged in as:{current_user}({'Master' if is_master else 'User'})")
    else: 
        messagebox.showerror("Login Failed", "Invalid credentials")
        root.quit()

def validate_user (username, password): 
    global is_master
    if not os.path.exists(user_file):
        return False 
    
    with open (user_file, newline ='') as f: 
        reader = csv.DictReader(f)
        for row in reader: 
            if row['username'] == username and row['password'] ==password: 
                is_master =row['is_master'].lower()=='true'
                return True
           
    return False

def clear_multiple_registration (): 
    id_username_entry.delete(0,tk.END)
    id_password_entry.delete(0,tk.END)
    id_confirm_entry.delete(0,tk.END)
    reg_is_master.set(False)
    
def clear_login_entry (): 
    login_username_entry.delete(0, tk.END)
    login_password_entry.delete(0, tk.END)
    
    


#Create directory if it doesn't exist
if not os.path.exists(csv_path):
    os.makedirs(csv_path)
    logging.info(f"Directory created: {csv_path}")
else:
    logging.info(f"Directory already exists: {csv_path}")
    
    #function to save data to CSV file 
def save_to_CSV(filename, headers, row):
    write_header =not os.path.exists(filename) or os.stat(filename).st_size ==0
    with open(filename, "a", newline ='') as f: 
        writer =csv.DictWriter(f,fieldnames=headers)
        if write_header:
            writer.writeheader()
        writer.writerow(row)
    
        
    '''df = pd.DataFrame([data])
    df.to_csv(lab_path, mode='a', index=False, header=not os.path.exists(lab_path) or os.stat(lab_path).st_size == 0)
    '''
    #Function to maintain the ID of each item registered
def unique_item_id(): 
    current_id =set()
    if os.path.exists(lab_path):
        df= pd.read_csv(lab_path)
        current_id = set(df['item_ID'].values)
    while True :
        new_id = f"VID_{random.randint(1000, 99999)}"
        if new_id not in current_id: 
            
            return new_id
         
         #Function to return page to the welcome page
def back_func():
    back_button= messagebox.askyesno("Back", "Do you want to return to welcome page?")
    if back_button: 
        return operation()
    else : 
            close() 
            # Function to close the loop
def close():
            cancel = messagebox.askyesno("Cancel", "Do you want to cancel?")
            if cancel: 
             logging.info("Operation cancelled by user.")
             exit()
tk.Button(root, text="Register", command=register_form).pack(pady=5)
tk.Button(root, text="Login", command=login_user).pack(pady=5) 
                   
# Inventory Operation
def operation():
    
        options = ["1.Register", "2. Add item", "3.Withdraw item", "4. Delete item", "5. View"]
        #Welcome page
    
        while True:
            option = simpledialog.askstring ("Input", "Welcome \n \n" + "\n \n".join(options)+ "\n \n Enter an option: ")
            if option is None:
                cancel = messagebox.askyesno("Cancel", "Do you want to cancel?")
                if cancel: 
                    logging.info("Operation cancelled by user.")
                    exit()
                else:
                    continue
            entries = {}
    

            if option not in ["1", "2", "3", "4", "5"]:
                logging.error("Invalid input.")
                messagebox.showinfo("Info", "Enter a Valid Option")
                option = simpledialog.askstring("Input", "\n".join(options) + "\n \n Enter your choice:")
                continue     

        #Option 1 
            if option == "1":
                labels = ["Item Name", "Item Description","Category", "Source"]
               #Option 1 Panel
                for i,label in enumerate(labels):
                    label_x = ttk.Label(top, text=label)
                    label_x.grid(row=i, column=0, padx=10, pady= 5, sticky="w")
                    entry = ttk.Entry(top, width=30)
                    entry.grid(row=i, column=1, padx=10, pady=5)
                    entries[label] = entry      
                #Submit function 
                def submit():
                    values = {labels:entry.get().strip() for labels, entry in entries. items()}
                    if not all (values.values()):
                        messagebox.showinfo("Error, Please enter all required fields")
                        return
                    quantity = simpledialog.askinteger("Quantity", "Enter Item Quatity:")#For inputing the quantity
                    if quantity is None: 
                        return 
                    #Update the entered data with generated ID and Date Entered
                    values.update({
                        "Username": current_user,
                        "item_ID" : unique_item_id(), 
                        "Date_Modified": datetime.now().strftime("%d-%m-%Y, %H:%M"),
                        "Item_Quantity": quantity
                        })
                    #All entered data saved
                    save_to_CSV(values)
                    messagebox.showinfo("Success, data saved successfully")
                    top.destroy()
                    back_func()
                    close ()
                # Submit           
                submit_btn = ttk.Button(top, text="Submit", command=submit)
                submit_btn.grid(row=len(labels), column=0, columnspan=4, pady=10, padx=[0,20])
                #Close 
                close_btn = ttk.Button(top, text="Close", command=close)
                close_btn.grid(row=len(labels), column=1, columnspan=4, pady=10, padx=[20,0])
                #for widget in top.winfo_children():
                    #widget.destroy()
                top.mainloop()
                 # Option 2   
            elif option == "2":
                values = {labels:entry.get().strip() for labels, entry in entries. items()}
                unique_item_id(),
                if not os.path.exists(lab_path):
                    messagebox.showinfo("Info", "No inventory file found.")
                    return

                #read saved Csv file 
                df = pd.read_csv(lab_path)
                x = simpledialog.askstring("Input", "Enter Item ID:")
                if x is None:
                    return

                if x not in df['item_ID'].values: #ID is not found in the CSV 
                    messagebox.showinfo("Error", "Item ID not found.")
                    return

                expected_category = df.loc[df['item_ID'] == x, 'Category'].values[0] #Locate  ID and Category
                y = simpledialog.askstring("Input", "Enter Category:")
                if y is None:
                    return

                if y != expected_category:
                    messagebox.showinfo("Error", "Category does not match.")#if category does not match
                    return

                qty = simpledialog.askfloat("Input", "Enter quantity to add:")#Add the amount of item to be added
                if qty is None or qty <= 0:
                    messagebox.showinfo("Error", "Invalid quantity.")
                    return

                # Convert and update
                df['Item_Quantity'] = pd.to_numeric(df['Item_Quantity'], errors='coerce').fillna(0)
                df.loc[df['item_ID'] == x, 'Item_Quantity'] += qty
                df.to_csv(lab_path, index=False)
                if not is_master: 
                    df =df[df['Username']==current_user]

                item_name = df.loc[df['item_ID'] == x, 'Item Name'].values[0]#Display Item info and the updated quantity
                total_qty = df.loc[df['item_ID'] == x, 'Item_Quantity'].values[0]
                messagebox.showinfo("Info", f"{item_name} total quantity is now: {total_qty}")
                save_to_CSV(values)
                messagebox.showinfo("Success, data saved successfully")
                back_func()
                close()
                # Submit           
                #submit_btn = ttk.Button(top, text="Submit", command=submit)
                #submit_btn.grid(row=len(labels), column=0, columnspan=4, pady=10, padx=[0,20])              
                        #close
                #close_btn = ttk.Button(top, text="Close", command=close)
                #close_btn.grid(row=len(labels), column=1, columnspan=4, pady=10, padx=[20,0])
                        
                top.mainloop()
            elif option == 3 : ## Option 3
                if not os.path.exists(lab_path):
                    messagebox.showinfo("Info", "No inventory file found.")
                    return 
                df =pd.read_csv(lab_path)
                x = simpledialog.askstring("Input", "Enter Item ID:")#Enter ID to locate Item
                if x is None or x not in df['item_ID'].values:
                    messagebox.showinfo("Error", "Item ID not found.")#Wrong Input
                    return
                available_qty = float(df.loc[df['item_ID'] == x, 'Item_Quantity'].values[0])#Locate Item Id and the quantity of Item
                name = df.loc[df['item_ID'] == x, 'Item Name'].values[0]
    
                while True:
                    qty = simpledialog.askfloat("Input", "Enter amount to Withdraw:") 
                    if qty is None: 
                        cancel =messagebox.askyesno("Cancel, Do you want to cancel?")
                        if cancel: 
                            logging.info("Operation cancelled by user.")
                            return
                        else: 
                            continue
                    if qty <= 0: #For quantity less than 0 
                        logging.error("Invalid input.")
                        messagebox.showinfo("Info", "Enter valid Amount")
                        #qty = simpledialog.askfloat("Input", "Enter the quantity to withdraw:")
                        continue
                    if qty > available_qty:
                        logging.error("Item Unavailable")
                        messagebox.showinfo("Info", f"Only{available_qty} is available")
                    # qty = simpledialog.askfloat("Input", "Enter the quantity to withdraw")
                        continue
                    #break 
                    df.loc[df['item_ID']== x, 'Item_Quantity']-= qty #Locate Item ID and remove the quantity removed
                    df.to_csv(os.path.join(csv_path, 'Lab.csv'), index = False)#Saves updates
                    if not is_master: 
                        df =df[df['Username']==current_user]

                    
                    new_qty = df.loc[df['item_ID']== x, 'Item_Quantity'].values[0] 
                    messagebox.showinfo("Info", f"{name} The total item is :{new_qty}")#Displays the remaining quantity
                    logging.info("Item Withdrawn Successfully") 
                    back_func()
                    close()  
                    top.mainloop()
            elif option == 5:
                    unique_item_id()
                    if not os.path .exists(lab_path):
                        messagebox.showinfo("Info,No inventory file found!")
                    return
                
            df =pd.read_csv(lab_path)
            x = simpledialog.askstring("Input", "Enter Item ID:")#Enter ID to locate Item
            if x is None or x not in df['item_ID'].values:
                    messagebox.showinfo("Error", "Item ID not found.")#Wrong Input
                    return
            name = df.loc[df['item_ID'] == x, 'Item Name'].values[0]
            iDescription = df.loc[df['item_ID' ]== x, 'Item Description'].values[0]
            new_qty = df.loc[df['item_ID']== x, 'Item_Quantity'].values[0]
            expected_category = df.loc[df['item_ID'] == x, 'Category'].values[0]
            
            iD_modi = datetime.now().strftime("%d-%m-%Y, %H:%M")
            messagebox.showinfo("info", f"The item details include :\n Name  : {name} \n Category:  {expected_category},  \n Description: {iDescription},\n Quantity:{new_qty} ")  
            logging.info("Item details fetched.")
            back_func()
            close() 
            break
            #top.destroy()       
            
#Closing Function
def close():
    logging.info("Exiting ...")
    root.destroy()
    exit()

# Main function
def main():
    root.deiconify()
    choice =messagebox.askquestion("Welcome", "Do you want t register a new user?")
    if choice =='yes': 
        register_form()
    #login_window()
    operation()
    close()

# Main Execution
if __name__ == "__main__":
    main()