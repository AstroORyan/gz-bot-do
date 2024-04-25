## Imports
from atproto import Client

import pandas as pd
import numpy as np
import requests
from io import BytesIO

import os

## Functions 
def pull_galaxy_image(url):
    response = requests.get(url)
    img_data = BytesIO(response.content)
    return img_data 

def create_metadata(row):
    z = row.redshift.iloc[0]
    ra = np.round(row.RA.iloc[0], 3)
    dec = np.round(row.DEC.iloc[0], 3)
    clsf = row.galaxy_description.iloc[0]
    survey = row.imaging.iloc[0]
    project = row.project.iloc[0]
    if 'Hubble' in project:
        instr = 'Hubble Space Telescope'

    metadata = (
"""A {}, observed with the {} in the {}.

It is at redshift {} and coordinates ({}, {}).

This classification was made in the {} project.
""").format(
            clsf, instr, survey, z, ra, dec, project
        )

    return metadata

def post(image, metadata, client):

    response = client.send_image(text = metadata, image = image, image_alt = 'A Galaxy')

    if len(response.errors) > 0:
        print("error posting to BlueSky -- errors:")
        print(response.errors)
    else:
        print("successfully posted animation")
    
    return response

## Main Function
def main():
    # Initialising connection to the BlueSky Client.
    client = Client()

    # Getting log in details
    usrname = os.getenv.get('USERNAME')
    pwd = os.getenv.get('PWD')
    cat_path = os.getenv.get('CAT_PATH')
    _ = client.login(usrname, pwd)

    # Selecting a Galaxy to upload.
    gal_row = pd.read_csv(cat_path).sample(1)
    url = gal_row['url']

    # Creating the Post
    image = pull_galaxy_image(url)
    post_string = create_metadata(gal_row)

    # Posting
    response = post(image, post_string, client)
    print(response)

## Initialisation
if __name__ == '__main__':
    main()