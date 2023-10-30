#Import all the necessary libraries
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
from tkinter import ttk
import csv
import tkinter as tk
import sys
import os


#Define the working of the button
def my_command(actionName):
   messagebox.askokcancel("Play movie", "Play movie - "+actionName)

#define read data
def read_data():
   with open(filename, 'r') as file:
       csvreader = csv.reader(file)
       header = next(csvreader)
       for row in csvreader:
           rows.append(row)


def select_provider(event):
    global provider_selected_idx
    provider_selected_idx = provider_combo.current()
#    print ("provider_selected_idx after "+str(provider_selected_idx))


#Define create buttons
def create_movie_buttons():
   global match_actor 
   global actor_entered
   global match_director
   global director_entered
   global match_year
   global year_entered
   
   clear_results(buttonList,btn_imgs)

   count_matched = 0
 
   # referring to their index numbers using the range(len(iterable))
   #0id	1Netflix	2Disney+	3Stan	4Binge	5Name	6Directors	7Main Characters	8Year Release	9Categories	10length in mins

   for i in range(len(rows)):
       match_found = False
       '''
       print ("idx "+str(provider_selected_idx))
       print ("provider "+ str(rows[i][provider_selected_idx+1]))
       print ("selected index")
       print (str(rows[i][provider_selected_idx+1] == 1))
       '''
       if rows[i][provider_selected_idx+1] == "1":
          
           director_entered = False
           if len(director_var.get("1.0","end-1c").strip())>0 :
              director_entered = True
              if " "+director_var.get("1.0","end-1c").strip().upper()+" " in " "+rows[i][6].strip().upper()+" ":
                  match_director = True
              else:
                  match_director = False

           actor_entered = False
           if len(actor_var.get("1.0","end-1c").strip())>0:
              actor_entered = True
              if " "+actor_var.get("1.0","end-1c").strip().upper()+" " in " "+rows[i][7].strip().upper()+" ":
                  match_actor = True
              else:
                  match_actor = False              

           year_entered = False
           if len(year_var.get("1.0","end-1c").strip())>0 :
              year_entered = True
              if year_var.get("1.0","end-1c").strip() == rows[i][8].strip():
                  match_year = True
              else:
                  match_year = False


           if ((match_director == True) or (director_entered == False)) and ((match_actor == True) or (actor_entered == False)) and ((match_year == True) or (year_entered == False )):
               #print("inputed text matched or all empty")
               if len(selected_catagories)==0:
                  match_found = True
                  count_matched = count_matched + 1
               else:
   
                  match_found = False
                  for n in range(len(selected_catagories)):

                     if selected_catagories[n].upper() in rows[i][9].upper() :
                        match_found = True
                        count_matched = count_matched + 1
                        #print ("matched")
                        break

           else:
              match_found = False
           
           if match_found == True:
              tmp_image = Image.open(current_location+'/images/'+ rows[i][0] +'.png')
              resized_image = tmp_image.resize((150,200))
              btn_image = ImageTk.PhotoImage(resized_image)
              btn_imgs.append(btn_image)


              btn = Button(frame_buttons, image=btn_image, command=lambda i=i:my_command(actionName=rows[i][5]),height= 180, width=135)
              btn.grid( row= ( (count_matched-1) // 5)+1  , column= ((count_matched-1) % 5), padx=8,pady=8, sticky="w")
              '''
              print("matched : " + str(count_matched ) )
              print("row : " + str(((count_matched-1) // 5)+1 ))
              print("column : " + str(((count_matched-1) % 5)))
              '''
              buttonList.append(btn)
# Update buttons frames idle tasks to let tkinter calculate buttons sizes
   frame_buttons.update_idletasks()
   canvas.config(scrollregion=canvas.bbox("all"))
   if count_matched == 0:
        messagebox.showinfo("info", "No matches found")
    

def clear_all(blst,ilst,slst):
      for chk in check_boxes:
         chk.state(['!selected'] )

      for itm in slst:
         slst.remove(itm)

      director_var.delete('1.0',tk.END)
      actor_var.delete('1.0',tk.END)
      year_var.delete('1.0',tk.END)
      
      for btn in blst:
         btn.destroy()
      del blst[:]  # also delete buttons from the list
      del ilst[:]

      #frame_buttons.config(bg="")

def clear_results(blst,ilst):
      for btn in blst:
         btn.destroy()
      del blst[:]  # also delete buttons from the list
      del ilst[:]
      #frame_buttons.config(bg="")

def value_changed(lst, element):
   if element in lst:
      lst.remove(element)
   else:
      lst.append(element)

def create_checkboxes():

   for i in range(len(movie_catagories)):
      check_box=ttk.Checkbutton(catagories_rectangle,text=movie_catagories[i],variable=movie_catagories[i],command=lambda
      x=movie_catagories[i] : value_changed(selected_catagories, x),width="10")
      check_box.state(['!alternate'])
      check_boxes.append(check_box)
      check_box.grid( row= ( i // 6) + 1 , column= i % 6,
      padx=10,pady=10, sticky="w")


# main

if getattr(sys, 'frozen', False):
    current_location = sys.executable
else:
    current_location = os.path.abspath(__file__)
current_location = os.path.dirname(current_location) 
#print("ex  :  "+current_location )


# csv file name
filename = current_location+"/Data/movieData.csv"


#Define the tkinter instance
win= Tk()
win.title("MUMBLE")


#Define the size of the tkinter frame
win.geometry("842x1400")
# global variables


buttonList =[]
btn_imgs=[]

# ["Animation" "Horror", "Romance", "Thriller", "Comedy", "Action", "Adventure", "Documentary", "Western", "Science fiction", "Crime film", "World cinema", "Drama"]
movie_catagories = ["Animation", "Horror", "Romance", "Thriller", "Comedy", "Action", "Adventure", "Documentary", "Western", "Science fiction", "Crime film", "World cinema", "Drama"]
selected_catagories = []
rows=[]
check_boxes = []
provider_selected_idx=0
match_actor = False
actor_entered = False
match_director = False
director_entered = False
match_year = False
year_entered = False

#providers_rectangle
providers_rectangle = tk.Frame(win,  highlightthickness=1, width = 800, height = 15,borderwidth=2, relief=tk.RIDGE )
providers_rectangle.configure(height=providers_rectangle["height"],width=providers_rectangle["width"])
providers_rectangle.grid_propagate(0)
providers_rectangle.grid(row=0, column=0, columnspan=3, ipadx=20, ipady=20,sticky="w")
label01 = Label(providers_rectangle, text="Streaming service")
label01.grid(row=0,column=0, padx=2,pady=0, sticky="w")
#create providers combobox
provider_combo = ttk.Combobox(providers_rectangle, values=["Netflix", "Disney+", "Stan", "Binge"])
provider_combo.current(0)
provider_combo.grid(padx=10,pady=0,row=1,column=0)
provider_combo.bind("<<ComboboxSelected>>", select_provider)

#catagories_rectangle 
catagories_rectangle = tk.Frame(win,  highlightthickness=1, width = 800, height = 100,borderwidth=2, relief=tk.RIDGE )
catagories_rectangle.configure(height=catagories_rectangle["height"],width=catagories_rectangle["width"])
catagories_rectangle.grid_propagate(0)
catagories_rectangle.grid(row=1, column=0, columnspan=3, ipadx=20, ipady=20,sticky="w")
label02 = Label(catagories_rectangle, text="Catagories")
label02.grid(row=0,column=0, padx=2,pady=0, sticky="w")

#director_rectangle 
director_rectangle = tk.Frame(win,  highlightthickness=1, width = 800, height = 14,borderwidth=2, relief=tk.RIDGE )
director_rectangle.configure(height=director_rectangle["height"],width=director_rectangle["width"])
director_rectangle.grid_propagate(0)
director_rectangle.grid(row=2, column=0, columnspan=3, ipadx=20, ipady=20,sticky="w")
label03 = Label(director_rectangle, text="Director")
label03.grid(row=0,column=0, padx=2,pady=0, sticky="w")
director_var = tk.Text(director_rectangle, height = 1, width = 50) 
director_var.grid(padx=10,pady=0, row=1,column=0)

#actor_rectangle 
actor_rectangle = tk.Frame(win,  highlightthickness=1, width = 800, height = 14,borderwidth=2, relief=tk.RIDGE )
actor_rectangle.configure(height=actor_rectangle["height"],width=actor_rectangle["width"])
actor_rectangle.grid_propagate(0)
actor_rectangle.grid(row=3, column=0, columnspan=3, ipadx=20, ipady=20,sticky="w")
label04 = Label(actor_rectangle, text="Actress/Actor")
label04.grid(row=0,column=0, padx=2,pady=0, sticky="w")
actor_var = tk.Text(actor_rectangle, height = 1, width = 50) 
actor_var.grid(padx=10,pady=0, row=1,column=0)

#year_rectangle 
year_rectangle = tk.Frame(win,  highlightthickness=1, width = 800, height = 14,borderwidth=2, relief=tk.RIDGE )
year_rectangle.configure(height=year_rectangle["height"],width=year_rectangle["width"])
year_rectangle.grid_propagate(0)
year_rectangle.grid(row=4, column=0, columnspan=3, ipadx=20, ipady=20,sticky="w")
label05 = Label(year_rectangle, text="Year")
label05.grid(row=0,column=0, padx=2,pady=0, sticky="w")
year_var = tk.Text(year_rectangle, height = 1, width = 14)
year_var.grid(padx=10,pady=0, row=1,column=0)

#suggest button and clear button
buttons_rectangle = tk.Frame(win,  highlightthickness=1, width = 800, height = 20, borderwidth=0, relief=tk.RIDGE )
buttons_rectangle.configure(height=buttons_rectangle["height"],width=buttons_rectangle["width"])
buttons_rectangle.grid_propagate(0)
buttons_rectangle.grid(row=5, column=0, columnspan=3, ipadx=20, ipady=5)

#Button(win, text='show', command=lambda i=i:messagebox.showinfo(title='Result',message=selected_catagories)).place(x=500,y=500)
suggest_button = Button(buttons_rectangle, text='Suggest', command=lambda:create_movie_buttons())
suggest_button.grid(row=0,column=0, padx=2,pady=0)

clear_button= Button(buttons_rectangle, text='Clear', command=lambda :clear_all(buttonList,btn_imgs,selected_catagories))
clear_button.grid(row=0,column=2, padx=2,pady=0)


#results_rectangle 
results_rectangle = tk.Frame(win, highlightthickness=1, width = 800, height = 200,borderwidth=0,relief=tk.RIDGE)
results_rectangle.grid(row=6, column=0, columnspan=3, ipadx=20, ipady=5,sticky="w")
#label05 = Label(results_rectangle, text="Suggestions")
#label05.grid(row=0,column=0, padx=2,pady=0,sticky="w")
# Add a canvas in that frame
canvas = tk.Canvas(results_rectangle, width = 800, height = 300)
canvas.grid(row=0, column=0, sticky="news")
# Link a scrollbar to the canvas
vsb = tk.Scrollbar(results_rectangle, orient="vertical", command=canvas.yview)
vsb.grid(row=0, column=1, sticky='ns')
canvas.configure(yscrollcommand=vsb.set)
# Create a frame to contain the result buttons
frame_buttons = tk.Frame(canvas, bg="")
canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

# read data from csv
read_data()

# create checkboxes
create_checkboxes()


win.mainloop()
