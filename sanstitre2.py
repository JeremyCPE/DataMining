from pandas.io.json import json_normalize
import pandas as pd
import json, re
from sklearn import tree
from sklearn.preprocessing import LabelEncoder
import webcolors
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plot
from operator import itemgetter
from PIL import ImageColor

#---------------- GET COLOR NAME FROM HEX VALUE -----------------#

def closestColor(requested_colour):
    COLOR_NAMES_TO_HEX = {
    "aqua": "#00ffff",
    "black": "#000000",
    "blue": "#0000ff",
    "fuchsia": "#ff00ff",
    #"maroon": "#800000",
    "red": "#ff0000",
    "white": "#ffffff",
    "yellow": "#ffff00",
    }
    min_colours = {}
    for colorKey in COLOR_NAMES_TO_HEX:
        colorHex = COLOR_NAMES_TO_HEX[colorKey]
        r_c, g_c, b_c = webcolors.hex_to_rgb(colorHex)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = colorKey
    return min_colours[min(min_colours.keys())]

def getColorName(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closestColor(requested_colour)
        actual_name = None
    return actual_name, closest_name

#---------------------------------------------------------------#

def getArrayPictures(jsonData):
    return jsonData["pictures"]

def openJsonFile(path):
    with open(path, "r") as jsonFile:
        try:
            return json.load(jsonFile)
        except:
            print("Erreur lors de l'ouverture du fichier 'project/data.json' ...")
            return 1
    
def verifyPseudo(pseudo, jsonData):
    usernames = list(map(itemgetter('username'), jsonData["users"])) 
    if(pseudo in usernames):
        return 0
    else:
        return 1

def addUsernameOnJsonFile(pseudo,jsondata):
    data = {"username": pseudo, "favorites": []}
    jsondata['users'].append(data)
    with open("project/data.json", "w") as jsonFile:
            json.dump(jsondata, jsonFile)
    
def pseudoConnectionChoice():
    pseudo = ""
    while True:
        pseudo = input("Quel est votre pseudo ?")
        if re.match("^[A-Za-z0-9_-]*$", pseudo):
            break  
        else:
            print("Seuls les lettres, les nombres, le caractère '-' et le caractère '_' sont acceptés.")
    return pseudo
    
def createAccountFeature(jsonData):
    pseudo = pseudoConnectionChoice()
    jsonData = ""
    if verifyPseudo(pseudo, jsonData) == 0:
            print("Ce pseudo est déjà existant dans la base de donnée, veuillez en saisir un nouveau")
            return 1
    else:
        addUsernameOnJsonFile(pseudo,jsonData)

def connectionFeature(jsonData):
    pseudo = pseudoConnectionChoice()
    if verifyPseudo(pseudo, jsonData) == 1:
            print("Ce pseudo ne correspond à aucune entrée dans la base de données...")
            return 1
    return pseudo

def getFavoriteIDsPictures(PSEUDO, users):
    for user in users:
        if user["username"] == PSEUDO:
            if len(user["favorites"]) == 0:
                print("Aucune image mise en favori pour l'utilisateur " + PSEUDO + " ...")
                return 1
            return user["favorites"]
    print("Impossible de récupérer les images favorites du pseudo " + PSEUDO + " ...")
    return 1

def getDataframedPictures(arrayPictures):
    if len(arrayPictures) < 1:
        print("Aucune image dans le jeu de données...")
        return 1
    listDataframedPictures = []
    for picture in arrayPictures:
        listDataFrame = []
        actualColorName, closestColorName = getColorName(ImageColor.getrgb(picture["color"]))
        listDataFrame.append(closestColorName if (actualColorName == None) else actualColorName)
        for tag in picture["tag"]:
            listDataFrame.append(tag)
        listDataFrame.append(picture["size"])
        listDataframedPictures.append(listDataFrame)
    return listDataframedPictures

def getFavoriteSampleArray(arrayIDsFavoritePictures):
    if len(arrayIDsFavoritePictures) < 1:
        print("Aucune image mise en favori...")
        return 1
    favoriteSampleArray = []
    for i in range(10):
        if (i+1) in arrayIDsFavoritePictures:
            favoriteSampleArray.append("favorite")
        else:
            favoriteSampleArray.append("notfavorite")
    return favoriteSampleArray  
    
def getFramesAndLabelsEncoder(data, result):
    dataframe = pd.DataFrame(data, columns=['color', 'tag1', 'tag2', 'tag3', 'sizeW'])
    resultframe = pd.DataFrame(result, columns=['favorite'])
    return dataframe, resultframe
    
def __main__():
    PSEUDO = ""
    while True:
        choix = input("Que voulez-vous faire ? (1: création de compte | 2: connexion)")
        if choix in ["1", "2"]:
            break
        else:
            print("Saisie invalide, veuillez choisir entre 1 et 2.")    
    #Ouverture du fichier JSON (une seule fois)
    jsonData = openJsonFile("project/data.json")
    if jsonData == 1:
        return 1
    # Action selon le choix de l'utilisateur
    if choix == "1":
        ret = createAccountFeature(jsonData)
        return ret
    else:
        PSEUDO = connectionFeature(jsonData)
        if PSEUDO == 1:
            return 1
    arrayPictures = getArrayPictures(jsonData)
    # Récupération des ID d'images favorites
    arrayIDsFavoritePictures = getFavoriteIDsPictures(PSEUDO, jsonData["users"])
    if arrayIDsFavoritePictures == 1:
        return 1
    # Récupération des images favorites selon les ID récupérés précédemment
    listDataframedPictures = getDataframedPictures(arrayPictures)
    if listDataframedPictures == 1:
        return 1
    print(listDataframedPictures)
    # Récupération du tableau booléen des images favorites/non favorites
    favoriteSampleArray = getFavoriteSampleArray(arrayIDsFavoritePictures)
    if favoriteSampleArray == 1:
        return 1
    print(favoriteSampleArray)
    
    # Création du dataframe et du resultframe
    dataframe, resultframe = getFramesAndLabelsEncoder(listDataframedPictures, favoriteSampleArray)
    print(dataframe.to_string())
    print("result =", resultframe)
    
    # Création des LabelEncoder
    le1 = LabelEncoder()
    dataframe['color'] = le1.fit_transform(dataframe['color'])
    le2 = LabelEncoder()
    dataframe['tag1'] = le2.fit_transform(dataframe['tag1'])
    le3 = LabelEncoder()
    dataframe['tag2'] = le3.fit_transform(dataframe['tag2'])
    le4 = LabelEncoder()
    dataframe['tag3'] = le4.fit_transform(dataframe['tag3'])
    le5 = LabelEncoder()
    dataframe['sizeW'] = le5.fit_transform(dataframe['sizeW'])
    le6 = LabelEncoder()
    #dataframe['sizeH'] = le6.fit_transform(dataframe['sizeH'])
    le7 = LabelEncoder()
    resultframe['favorite'] = le7.fit_transform(resultframe['favorite'])
    
    #Use of random forest classifier
    rfc = RandomForestClassifier(n_estimators=10, max_depth=2,
                             random_state=0)
    rfc = rfc.fit(dataframe, resultframe.values.ravel())
    
    #prediction
    prediction = rfc.predict([
    [le1.transform(['gray'])[0], le2.transform(['bieres'])[0],
     le3.transform(['photo'])[0], le4.transform(['discotheque'])[0], le5.transform([640])[0],le6.transform([800])[0]]])
    print(le7.inverse_transform(prediction))
    print(rfc.feature_importances_)
    
if __main__() == 1:
    print("Sortie du script...")
else:
    print("Script réalisé avec succès.")


