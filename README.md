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



if you get a 'ModuleNotFoundError: No module named 'cv2'' install opencv by typing following in the terminal
```
pip install opencv-python
```

