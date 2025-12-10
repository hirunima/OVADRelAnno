info_final folder can be downloaded from 'https://drive.google.com/drive/folders/1CLFNOKnYTwJ0ZBz9SVBFko4raKylGMNX?usp=drive_link'

ovad_images can be downloaded from 'https://drive.google.com/drive/folders/1iVmSnyECZt1uhEZ7Q8CDqBafflT1oYtT?usp=drive_link'

manual_checked_hirunima can be downloaded from 'https://drive.google.com/drive/folders/1lbOeL_Wm5pCoZc5_hCsVdFr30rL-lz79?usp=sharing'

Put all three folders in the running folder.

## Annotation tool

you get a two relationship suggestions from 'LLAVA' and 'QWEN'.

Relationship in the format of {subject, relation, object}

subject and object is deficted by a number which would belong to one of the entities inside the bounding boxes.

You have to detemine the given relation is correct with respect to the subject and the object.

you can see examples of bad relations in 'relation_list.py'--> 'bad_relations'. Relations should be simple and consious and should not include any physical objects

If both LLAVA relationship and the QWEN relationships are false, you can write a suggestion for the relation in the ''Better suggestion'' box. When writing the suggestion conside the relation between the entity with smallest id as the subject and the entity with largest id as the object.

## Running the script

You can run

```
python visualize_final_yourname.py
```
to get the annotation tool working

if you get a 'ModuleNotFoundError: No module named 'cv2'' install opencv by typing following in the terminal
```
pip install opencv-python
```

## Adding Missing Relation

You can run

```
python visualize_final_mahith.py
```
to get the annotation tool working. This would open the same annotation tool with same images you annotated but with different objects and relations between them. We are adding at least realtions for each object and adding extra relations for main objects.

You need to download one folder.

manual_checked folder can be downloaded from '[https://drive.google.com/drive/folders/1xzQm05v8-65kWTqvCDoKw_nyY68y-ftC?usp=sharing](https://drive.google.com/file/d/1-k0U3i_UfWusDpV3ZbeTMxntMfoIX5Hr/view?usp=drive_link)'

