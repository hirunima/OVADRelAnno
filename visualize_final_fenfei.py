
import json
from logging import root
import os
import numpy as np
import random
import cv2
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
from copy import deepcopy

def read_json_file(file_path):
    """
    Reads a JSON file and returns its content.
    
    :param file_path: Path to the JSON file.
    :return: Parsed JSON content as a dictionary.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return data

def extract_data(json_data):
    """
    Extracts attributes, categories, and annotations from the JSON data.
    
    :param json_data: Parsed JSON content.
    :return: Tuple containing extract data.
    """
    extracted_data ={}
    for i in json_data:
        extracted_data[i['id']] = []
        i_new=i['name'][i['name'].find(':')+1:]
        for j in i_new.split('/'):
            extracted_data[i['id']].append(j)
    return extracted_data
cat=''
bckg=''

def annotate_image(img, llava_item, relation, i, llava_items, qwen_items, obj1, obj2):
    root = tk.Tk()
    root.title("Annotation Tool")

    # --- Load and display image ---
    # img = Image.open(image_path)
    # img = img.resize((500, 400))  # resize if needed
    tk_img = ImageTk.PhotoImage(img)
    panel = tk.Label(root, image=tk_img)
    panel.pack(pady=10)

    # --- LLaVA Question ---
    tk.Label(root, text=f"LLaVA relationship: {obj1} is {llava_item['relationship']} to {obj2}").pack()
    llava_var = tk.StringVar(value="No")
    tk.Frame(root)
    tk.Button(root, text="Yes", command=lambda: llava_var.set("Yes")).pack(side="left", padx=5)
    tk.Button(root, text="No", command=lambda: llava_var.set("No")).pack(side="left", padx=5)

    # --- Qwen Question ---
    tk.Label(root, text=f"Qwen relationship: {obj1} is {relation} to {obj2}").pack(pady=(10, 0))
    qwen_var = tk.StringVar(value="No")
    tk.Button(root, text="Yes", command=lambda: qwen_var.set("Yes")).pack(side="left", padx=5)
    tk.Button(root, text="No", command=lambda: qwen_var.set("No")).pack(side="left", padx=5)

    # --- Human Suggestion ---
    tk.Label(root, text="Better suggestion?").pack(pady=(10, 0))
    human_var = tk.Entry(root, width=40)
    human_var.pack()

    def submit():
        llava_items[i]['relationship_correct'] = (llava_var.get() == "Yes")
        qwen_items[i]['relationship_correct'] = (qwen_var.get() == "Yes")
        qwen_items[i]['human'] = human_var.get()
        root.destroy()

    tk.Button(root, text="Submit", command=submit).pack(pady=10)
    root.mainloop()

def main():
    # Example usage

    info = './info_final/'
    inputs = sorted(os.listdir(info))
    image_path = './ovad_images/'# + file.replace('.json', '.png')  # Replace with your JSON file path
    hirunima_checked = './manual_checked_hirunima/'
    already = os.listdir(hirunima_checked)

    output_dir = './manual_checked/'
    os.makedirs(output_dir, exist_ok=True)
    already += os.listdir(output_dir)

    inputs = [f for f in inputs if f not in already]

        # save_path = os.path.join('/vulcanscratch/hirunima/ovad_images/', img_name)
        # os.makedirs(os.path.dirname(save_path), exist_ok=True)
    for file in reversed(inputs):
        file_path = os.path.join(info, file) 
        
        data = read_json_file(file_path)
        
        # cv2.imwrite(save_path, img)
        image_id = data['image_id']
        relations=[]
        objects = {}
        output = deepcopy(data)

        if len(data['items'])!=1:
            for item in data['items']:
                objects[item['object_id']] = item['category']
            objects_list = []
            for i,item in enumerate(data['items']):
            # for i, item in enumerate(items):
                
                category = item['category']
                closest_category = item['closest_category']
                if sorted((item['object_id'], item['closest_id'])) in objects_list:
                    continue
                # attributes = ', '.join(item['attributes'])
                objects_list.append(sorted((item['object_id'], item['closest_id'])))

                bbox = item['bbox']
                img_name = f"{image_id:012}.jpg"
                img_path = os.path.join(image_path, img_name)
                img_single = cv2.imread(img_path)
                
                
                # Draw bounding box on the image
                x, y, w, h = map(int, bbox)
                cv2.rectangle(img_single, (x, y), (x + w, y + h), (0, 255, 0), 1)
                label = f"{item['category'], item['object_id']}"
                cv2.putText(img_single, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

                closest_bbox = item['closest_bbox']
                x, y, w, h = map(int, closest_bbox)
                cv2.rectangle(img_single, (x, y), (x + w, y + h), (0, 0, 255), 1)
                label_closest = f"{item['closest_category'], item['closest_id']}"
                

                cv2.putText(img_single, label_closest, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                img_single = cv2.resize(img_single, (600,400))

                img_org = cv2.imread(img_path)
                img_org = cv2.resize(img_org, (600,400))

                side_by_side = np.concatenate((img_single, img_org), axis=1)
                side_by_side_rgb = cv2.cvtColor(side_by_side, cv2.COLOR_BGR2RGB)
                im_pil = Image.fromarray(side_by_side_rgb)
                
                root = tk.Tk()
                root.title("Annotation Tool")

                # --- Load and display image ---
                tk_img = ImageTk.PhotoImage(im_pil)
                panel = tk.Label(root, image=tk_img)
                panel.pack(pady=10)

                # --- LLaVA Question ---
                llava_frame = tk.Frame(root)
                llava_frame.pack(pady=5)
                tk.Label(llava_frame, text=f"LLaVA relationship: {item['relationship_llava']}").pack(side="left")
                llava_var = tk.StringVar(value="No")
                tk.Button(llava_frame, text="Yes", command=lambda: llava_var.set("Yes")).pack(side="left", padx=5)
                tk.Button(llava_frame, text="No", command=lambda: llava_var.set("No")).pack(side="left", padx=5)
                

                # --- Qwen Question ---
                qwen_frame = tk.Frame(root)
                qwen_frame.pack(pady=5)
                tk.Label(qwen_frame, text=f"Qwen relationship: {item['relationship_qwen']}").pack(side="left")
                qwen_var = tk.StringVar(value="No")
                tk.Button(qwen_frame, text="Yes", command=lambda: qwen_var.set("Yes")).pack(side="left", padx=5)
                tk.Button(qwen_frame, text="No", command=lambda: qwen_var.set("No")).pack(side="left", padx=5)
                

                # --- Human Suggestion ---
                tk.Label(root, text="Better suggestion?").pack(pady=(10, 0))
                human_var = tk.Entry(root, width=40)
                human_var.pack()
                

                def submit():
                    output['items'][i]['llava_relationship_correct'] = (llava_var.get() == "Yes")
                    print('llava answer recorded',llava_var.get())
                    output['items'][i]['qwen_relationship_correct'] = (qwen_var.get() == "Yes")
                    print('qwen answer recorded',qwen_var.get())
                    output['items'][i]['human_suggestion'] = human_var.get()
                    print('human answer recorded',human_var.get())
                    root.destroy()
                    

                tk.Button(root, text="Submit", command=submit).pack(pady=10)
                root.mainloop()
                print('#################################')

        output_path = os.path.join(output_dir, f"{image_id:012}.json")
        
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
            # user_input = get_dropdown_selection(options)

            # relation_input = input('enter the realtion: ')
            # relation['relation'] = relation_input
            # relation['object'] = user_input

            # print(f"You entered: {relation}")
            # item['relations'] = relation

def get_dropdown_selection(options):
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    selected = simpledialog.askstring("Input", f"Choose the object: {', '.join(options)}")
    root.destroy()
    return selected            

if __name__ == "__main__":
    main()
    
