from google.cloud import vision

'''list_uri = ['gs://uncommon-hacks/IMG_0001.JPG', 'gs://uncommon-hacks/IMG_0002.JPG', 'gs://uncommon-hacks/IMG_0003.JPG',
            'gs://uncommon-hacks/IMG_0004.JPG', "gs://uncommon-hacks/IMG_0005.JPG", "gs://uncommon-hacks/IMG_0006.JPG",
            "gs://uncommon-hacks/IMG_0007.JPG", "gs://uncommon-hacks/IMG_0008.JPG", "gs://uncommon-hacks/IMG_0009.JPG", "gs://uncommon-hacks/IMG_0010.JPG",
            'gs://uncommon-hacks/IMG_0011.JPG', 'gs://uncommon-hacks/IMG_0012.JPG', 'gs://uncommon-hacks/IMG_0013.JPG',
            'gs://uncommon-hacks/IMG_0014.JPG', "gs://uncommon-hacks/IMG_0015.JPG", "gs://uncommon-hacks/IMG_0016.JPG",
            "gs://uncommon-hacks/IMG_0017.JPG", "gs://uncommon-hacks/IMG_0018.JPG", "gs://uncommon-hacks/IMG_0019.JPG", "gs://uncommon-hacks/IMG_0020.JPG",
            'gs://uncommon-hacks/IMG_0021.JPG', 'gs://uncommon-hacks/IMG_0022.JPG', 'gs://uncommon-hacks/IMG_0023.JPG',
            'gs://uncommon-hacks/IMG_0024.JPG', "gs://uncommon-hacks/IMG_0025.JPG", "gs://uncommon-hacks/IMG_0026.JPG",
            "gs://uncommon-hacks/IMG_0027.JPG", "gs://uncommon-hacks/IMG_0028.JPG", "gs://uncommon-hacks/IMG_0029.JPG", "gs://uncommon-hacks/IMG_0030.JPG",
            'gs://uncommon-hacks/IMG_0031.JPG', 'gs://uncommon-hacks/IMG_0032.JPG', 'gs://uncommon-hacks/IMG_0033.JPG',
            'gs://uncommon-hacks/IMG_0034.JPG', "gs://uncommon-hacks/IMG_0035.JPG", "gs://uncommon-hacks/IMG_0036.JPG",
            "gs://uncommon-hacks/IMG_0037.JPG", "gs://uncommon-hacks/IMG_0038.JPG", "gs://uncommon-hacks/IMG_0039.JPG", "gs://uncommon-hacks/IMG_0040.JPG"]'''

list_uri1 = ['gs://uncommon-hacks/IMG_0001.JPG', 'gs://uncommon-hacks/IMG_0002.JPG', 'gs://uncommon-hacks/IMG_0003.JPG',
            'gs://uncommon-hacks/IMG_0004.JPG', "gs://uncommon-hacks/IMG_0005.JPG", "gs://uncommon-hacks/IMG_0006.JPG",
            "gs://uncommon-hacks/IMG_0007.JPG", "gs://uncommon-hacks/IMG_0008.JPG", "gs://uncommon-hacks/IMG_0009.JPG", "gs://uncommon-hacks/IMG_0010.JPG", "gs://uncommon-hacks/IMG_0011.JPG"]
list_uri2 = ['gs://uncommon-hacks/IMG_0012.JPG', 'gs://uncommon-hacks/IMG_0013.JPG',
            'gs://uncommon-hacks/IMG_0014.JPG', "gs://uncommon-hacks/IMG_0015.JPG", "gs://uncommon-hacks/IMG_0016.JPG",
            "gs://uncommon-hacks/IMG_0017.JPG", "gs://uncommon-hacks/IMG_0018.JPG", "gs://uncommon-hacks/IMG_0019.JPG", "gs://uncommon-hacks/IMG_0020.JPG"]
list_uri3 = ['gs://uncommon-hacks/IMG_0021.JPG', 'gs://uncommon-hacks/IMG_0022.JPG', 'gs://uncommon-hacks/IMG_0023.JPG',
            'gs://uncommon-hacks/IMG_0024.JPG',  "gs://uncommon-hacks/IMG_0026.JPG",
            "gs://uncommon-hacks/IMG_0027.JPG", "gs://uncommon-hacks/IMG_0028.JPG", "gs://uncommon-hacks/IMG_0029.JPG", "gs://uncommon-hacks/IMG_0030.JPG", 'gs://uncommon-hacks/IMG_0031.JPG']
list_uri4 = ['gs://uncommon-hacks/IMG_0032.JPG', 'gs://uncommon-hacks/IMG_0033.JPG',
            'gs://uncommon-hacks/IMG_0034.JPG', "gs://uncommon-hacks/IMG_0035.JPG", "gs://uncommon-hacks/IMG_0036.JPG",
            "gs://uncommon-hacks/IMG_0037.JPG", "gs://uncommon-hacks/IMG_0038.JPG", "gs://uncommon-hacks/IMG_0039.JPG", "gs://uncommon-hacks/IMG_0040.JPG"]
list_uris = [list_uri1, list_uri2, list_uri3, list_uri4]

'''photo_dict = {}  # Photo uri as key, with labels as values.
label_dict = {}  # label name, % -- photo uri'''

prioritylabels = ['Glasses', 'Nightclub', 'Fun', 'Team', 'Face']

def returnimagefromcluster(cluster_photo_dict, prioritylabels):
    # sort the cluster by an array of (%, lablename, photo uri)
    clusterpics = []
    sortedclusterpics = []
    for pict, labeldata in cluster_photo_dict.items():
        for labelname, labelpercentage in labeldata.items():
            clusterpics.append((labelpercentage, labelname, pict))
    sortedclusterpics = sorted(clusterpics, key=lambda pic: pic[0], reverse=1)
    # print(sortedclusterpics)

    # return the image that is in prioritylabels
    for item in sortedclusterpics:
        if item[1] in prioritylabels:
            prioritylabels.remove(item[1])
            # print("this is:")
            # print(item)
            return item[2]

for j in list_uris:
    photo_dict = {}  # Photo uri as key, with labels as values.
    label_dict = {}  # label name, % -- photo uri
    for i in j:
        image_uri = i

        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = image_uri
        response = client.label_detection(image=image)

        list_desc_score_tuples = {}

        #print('Labels (and confidence score):')
        #print('=' * 79)
        #print(image_uri)
        for label in response.label_annotations:
            # list_desc_score_tuples.append((label.description,label.score))
            list_desc_score_tuples[label.description] = label.score
            #print(f'{label.description} ({label.score*100.:.2f}%)')

        # Add to dictionary
        photo_dict[image_uri] = list_desc_score_tuples
        #print(photo_dict[image_uri])


    finaluri = returnimagefromcluster(photo_dict, prioritylabels)
    print(finaluri)
