import json
from logging import root
import os
import numpy as np
import random
import cv2
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk

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

def annotate_image(img, llava_item, relation, i, llava_items, qwen_items):
    root = tk.Tk()
    root.title("Annotation Tool")

    # --- Load and display image ---
    # img = Image.open(image_path)
    # img = img.resize((500, 400))  # resize if needed
    tk_img = ImageTk.PhotoImage(img)
    panel = tk.Label(root, image=tk_img)
    panel.pack(pady=10)

    # --- LLaVA Question ---
    tk.Label(root, text=f"LLaVA relationship: {llava_item['relationship']}").pack()
    llava_var = tk.StringVar(value="No")
    tk.Frame(root)
    tk.Button(root, text="Yes", command=lambda: llava_var.set("Yes")).pack(side="left", padx=5)
    tk.Button(root, text="No", command=lambda: llava_var.set("No")).pack(side="left", padx=5)

    # --- Qwen Question ---
    tk.Label(root, text=f"Qwen relationship: {relation}").pack(pady=(10, 0))
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
    qwen='./info_qwen/'
    llava='./info_llava/'
    input_qwen = os.listdir(qwen)
    input_llava = os.listdir(llava)

        # save_path = os.path.join('/vulcanscratch/hirunima/ovad_images/', img_name)
        # os.makedirs(os.path.dirname(save_path), exist_ok=True)
    for file in input_qwen:
        if file not in input_llava:
            print('Please note down this file as it is not in llava', file)
        file_qwen = os.path.join(qwen, file)  # Replace with your JSON file path
        file_llava = os.path.join(llava, file)  # Replace with your JSON file path
        data_qwen = read_json_file(file_qwen)
        data_llava = read_json_file(file_llava)
        image_path = './ovad_images/'# + file.replace('.json', '.png')  # Replace with your JSON file path
        output_dir = './manual_checked/'
        os.makedirs(output_dir, exist_ok=True)
        # cv2.imwrite(save_path, img)
        image_id = data_llava['image_id']
        relations=[]
        objects = {}
        output = { "image_id": image_id, }

        if len(data_llava['items'])!=1:
            for item in data_llava['items']:
                objects[item['object_id']] = item['category']

            for i,(llava_item,qwen_item) in enumerate(zip(data_llava['items'],data_qwen['items'])):
            # for i, item in enumerate(items):
                
                category = llava_item['category']
                # attributes = ', '.join(item['attributes'])
                
                bbox = llava_item['bbox']
                img_name = f"{image_id:012}.jpg"
                img_path = os.path.join(image_path, img_name)
                img_single = cv2.imread(img_path)
                
                # Draw bounding box on the image
                x, y, w, h = map(int, bbox)
                cv2.rectangle(img_single, (x, y), (x + w, y + h), (0, 255, 0), 1)
                label = f"{llava_item['category'], llava_item['object_id']}"
                cv2.putText(img_single, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

                closest_bbox = llava_item['closest_bbox']
                x, y, w, h = map(int, closest_bbox)
                cv2.rectangle(img_single, (x, y), (x + w, y + h), (0, 0, 255), 1)
                label_closest = f"{llava_item['closest_category'], llava_item['closest_id']}"
                cv2.putText(img_single, label_closest, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

                side_by_side = np.concatenate((img_single, cv2.imread(img_path)), axis=1)
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
                tk.Label(llava_frame, text=f"LLaVA relationship: {llava_item['relationship']}").pack(side="left")
                llava_var = tk.StringVar(value="No")
                tk.Button(llava_frame, text="Yes", command=lambda: llava_var.set("Yes")).pack(side="left", padx=5)
                tk.Button(llava_frame, text="No", command=lambda: llava_var.set("No")).pack(side="left", padx=5)

                # --- Qwen Question ---
                qwen_frame = tk.Frame(root)
                qwen_frame.pack(pady=5)
                tk.Label(qwen_frame, text=f"Qwen relationship: {qwen_item['relationship']}").pack(side="left")
                qwen_var = tk.StringVar(value="No")
                tk.Button(qwen_frame, text="Yes", command=lambda: qwen_var.set("Yes")).pack(side="left", padx=5)
                tk.Button(qwen_frame, text="No", command=lambda: qwen_var.set("No")).pack(side="left", padx=5)

                # --- Human Suggestion ---
                tk.Label(root, text="Better suggestion?").pack(pady=(10, 0))
                human_var = tk.Entry(root, width=40)
                human_var.pack()

                def submit():
                    output['llava_relationship_correct'] = (llava_var.get() == "Yes")
                    output['qwen_relationship_correct'] = (qwen_var.get() == "Yes")
                    output['human_suggestion'] = human_var.get()
                    root.destroy()
                    

                tk.Button(root, text="Submit", command=submit).pack(pady=10)
                root.mainloop()
                
                output['llava_items'] = llava_item
                output['qwen_items'] = qwen_item
                output['category'] = category
                output['bbox'] = bbox
                output['image_path'] = img_path
                # output['attributes'] = attributes
                output['closest_object'] = llava_item['closest_category']
                output['closest_id'] = llava_item['closest_id']
                output['closest_bbox'] = llava_item['closest_bbox']
                output['objects'] = objects
        else:
            # output['category'] = data_llava['items']['category']
            # output['attributes'] = data_llava['items']['attributes']
            # output['bbox'] = data_llava['items']['bbox']
            output['image_path'] = data_llava['image_path']
            output['items'] = data_llava['items']


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
    