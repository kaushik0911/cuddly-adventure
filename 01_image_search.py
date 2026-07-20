# %%
import weaviate

# %%
client = weaviate.Client("http://localhost:8080")
print(f"Client created? {client.is_ready()}")


# %%
current_schemas = client.schema.get()['classes']

for schema in current_schemas:
    if schema['class']=='ClipExample':
        client.schema.delete_class('ClipExample')



# %%

class_obj = {
    "class": "ClipExample",
    "moduleConfig": {
        "multi2vec-clip": {"imageFields": ["image"]}
    },

    'vectorizer':"multi2vec-clip",

    "properties" : [{"name": "text", "dataType":["string"]},
                   {
                       "name": "image", 'dataType':["blob"]
                   }]
}

client.schema.create_class(class_obj)
print("Schema class created")
# %%
import os
#Add images to our created class

for img in os.listdir("Images/"):
    print(f"Images/{img}")

    encoded_image = weaviate.util.image_encoder_b64(f"Images/{img}")

    data_properties = {
        "image":encoded_image,
        "text": img
    }

    client.data_object.create(data_properties, "ClipExample")

print("All images added!")
# %%
#Lets search for images of "open sea beach"
import json

res = (client.query
       .get('ClipExample',['text',"_additional {distance} "])
       .with_near_text({"concepts":"open sea beach"})
       .with_limit(5)
       .do()
)

print(json.dumps(res,indent=2))
# %%
import IPython

#Lets visualize the images that came back
IPython.display.Image(filename='Images/Point Reyes_ California_LIL_9672.jpg',width=300)
# %%

#Search for another concept!

res = (client.query
       .get('ClipExample',['text',"_additional {distance} "])
       .with_near_text({"concepts":"greenery and trees"})
       .with_limit(5)
       .do()
)

print(json.dumps(res,indent=2))
# %%
#Lets visualize the images that came back
IPython.display.Image(filename='Images/Forest_LIL_134133.jpg',width=300)
# %%
#Lets look at another input image query

IPython.display.Image(filename='TestImages/Cat outside_LIL_134200.jpg',width=300)

# %%
res = (client.query
       .get('ClipExample',['text',"_additional {distance} "])
       .with_near_image({"image":'TestImages/Cat outside_LIL_134200.jpg'})
       .with_limit(5)
       .do()
)

print(json.dumps(res,indent=2))

# %%
IPython.display.Image(filename='Images/Cat_LIL_134138.jpg',width=300)
