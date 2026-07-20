# %%
import pickle, weaviate, json, os, IPython

# %%
#Connect to the locally launched instance of Weaviate

client = weaviate.Client("http://localhost:8080")

print(f"Client created? {client.is_ready()}")

# %%

#Delete the schema if it alredy exists
if client.schema.exists("TextImageSearch"):
    client.schema.delete_class("TextImageSearch")


# %%
#To do this we need to specify a schema in which we can specify the model to be used
# aswell as the properties.

class_obj = {
    'class':"TextImageSearch",
    'moduleConfig' :{
        'multi2vec-clip':{"imageFields":['image']}
    },

    'vectorizer': 'multi2vec-clip',

    'properties' : [{'name': "text", "dataType": ['string']},
                   {'name': 'image', "dataType": ['blob']}
                   ]
}

client.schema.create_class(class_obj)
print("Schema class created")

# %%

# Here we will pass in a larger dataset into a folder called "Images"

#If you'd like to add your own images to the vector database to search over
# feel free to add them into this folder aswell!

for img in os.listdir("Images/"):

    print(f"Adding image: {img}")

    encoded_image = weaviate.util.image_encoder_b64(f'Images/{img}')

    data_properties = {
        'image': encoded_image,
        'text' : img
    }

    client.data_object.create(data_properties, class_name="TextImageSearch")

print("All images added!")
# %%

# Search the data with a text query

res = (
    client.query
    .get("TextImageSearch", ['text', '_additional {distance}'])
    .with_near_text({'concepts':['cute cats outdoors']})
    .with_limit(3)
    .do()
)

print(json.dumps(res,indent=2))

# %%
IPython.display.Image(filename='Images/Cats on a chair_LIL_134151.jpg', width=300)
