import dearpygui.dearpygui as dpg #pip install dearpygui
import cv2 #pip install opencv-python
import os

face_features = cv2.CascadeClassifier("features/frontal_face_haarcascade.xml")
selected_folder = None
drawed = []
results = []
dpg.create_context()

def callback(sender, data): #OK button
    global selected_folder
    selected_folder = data['current_path']
    dpg.set_value("selected_folder", ("Selected path: " + selected_folder))

def button_click(sender, data):
    global selected_folder, updater, results
    if(selected_folder != None):
        files = []
        results = [] #file paths of recognised images with faces
        for image in os.listdir(selected_folder):
            if(image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg") or image.endswith(".bmp")):
                files.append((cv2.imread(selected_folder + '/' + image), selected_folder + '/' + image)) #firt is image and second is path     

        global drawed 
        drawed = []       
        for i in files:
            temp_faces = [] #list to hold how many faces was found
            resized = cv2.resize(i[0], (960, 554), cv2.INTER_AREA)
            grayscaled = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            temp_faces = face_features.detectMultiScale(grayscaled, 1.6)
            for (x, y, w, h) in temp_faces:
                cv2.rectangle(resized, (x, y), (x+w, y+h), (255, 0 , 0), 2)             
            if len(temp_faces) > 0:           
                drawed.append(resized)
                results.append(i[1])
        if len(results) > 0:         
            dpg.set_value("status", "Found faces in images:")
        else: dpg.set_value("status", "Faces were not found!")
        dpg.configure_item("result", items=results)

            

def myfunc(sender):
    index = results.index(dpg.get_value(sender))
    cv2.imshow(f"{dpg.get_value(sender)}", drawed[index])
    cv2.waitKey(0)     

dpg.add_file_dialog(
    directory_selector=True, height=300, width=600, show=False, callback=callback, tag="file_dialog_id")

with dpg.theme() as new_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (135,67,15,255)) #(r,g,b,a)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (200,119,0,153))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (236,159,29,103))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (236,187,29,103))
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (236,159,29,103))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (236,187,29,103))
        dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (236,159,29,103))

with dpg.window(label="FaceFounder", width=800, height=450, tag="primary"):
    dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_text(tag="selected_folder", default_value="Selected path: None")
    dpg.add_text(tag="status")
    dpg.add_button(label="Find faces", callback=button_click)
    dpg.add_listbox(tag="result", callback=myfunc,  num_items=5)

dpg.bind_theme(new_theme)

dpg.create_viewport(title='Window1', height=450, width=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary", True)
dpg.start_dearpygui()
dpg.destroy_context()