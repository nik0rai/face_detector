import dearpygui.dearpygui as dpg #pip install dearpygui
import cv2 #pip install opencv-python
import os

face_features = cv2.CascadeClassifier("features/frontal_face_haarcascade.xml")
selected_folder = None

dpg.create_context()

def callback(sender, data): #OK button
    global selected_folder
    selected_folder = data['current_path']
    dpg.set_value("selected_folder", selected_folder)

def button_click(sender, data):
    global selected_folder
    if(selected_folder != None):
        files = []
        results = [] #file paths of recognised images with faces
        for image in os.listdir(selected_folder):
            if(image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg") or image.endswith(".bmp")):
                files.append((cv2.imread(selected_folder + '/' + image), image)) #firt is image and second is path       
        for x in files:
            temp_faces = [] #list to hold how many faces was found
            resized = cv2.resize(x[0], (960, 554), cv2.INTER_AREA)
            grayscaled = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            temp_faces = face_features.detectMultiScale(grayscaled, 1.6)
            if len(temp_faces) > 0:
                results.append(x[1])
        if len(results) > 0:         
            dpg.set_value("result", f"Found faces in these photos: {results}")
        else: dpg.set_value("result", "No faces were found!")
            

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

with dpg.window(label="FaceFounder", width=800, height=400, tag="primary"):
    dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_text(tag="selected_folder", default_value="Selected directory: none")
    dpg.add_button(label="Find faces", callback=button_click)
    dpg.add_text(tag="result", default_value="")

dpg.bind_theme(new_theme)

dpg.create_viewport(title='Window1', width=800, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary", True)
dpg.start_dearpygui()
dpg.destroy_context()