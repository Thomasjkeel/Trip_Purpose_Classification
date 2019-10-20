# required libraries
import sys
import geopandas as gpd # v0.4.0+26.g9e584cc
import pandas as pd

# GLOBALS
PURPOSE_TRANSLATIONS = {"None":"None",'Reconduire / aller chercher une personne':'pick_up_drop_off',
       "Travail / Rendez-vous d'affaires":'work', 'Magasinage / emplettes':'shops',
       'Retourner à mon domicile':'returning_home', 'Santé':'health', 'Loisir':'leisure', 'Éducation':'education',
       'Autre':'other', 'Repas / collation / café':'food_drink', 'ND':'not_available',"Retour Ã\xa0 la maison":"returning_home",
                       "Travail":"work","DÃ©poser / Ramasser":"pick_up_drop_off","Repas / collation /cafÃ©":"food_drink",
                       "Magasinage / Commission":"shops","Ã\x89ducation":"education","SantÃ©":"health",
                        "RÃ©union pour le travail":"work"}
## NOTE: 'meeting for work' has been re-classified as 'work' (1,258 trips)

MODE_TRANSLATIONS = {"Voiture / Moto":"car", "À pied":"walking", "Transport collectif":"public_transport",
                     "Autopartage":"car_sharing", "Vélo":"cycling", "Taxi":"taxi",
                     "Autre":"other", "ND":"not_available", "Ã\x80 pied":"walking", "Autre combinaison":"combination",
                    "Transport Collectif":"public_transport", "Automobile":"car","VÃ©lo":"cycling",
                     "Automobile et transport collectif":"public_transport, car","Autre mode":"other"}


def mode_to_new_name(mode_names):
        """
        translates a string, potentially containing a list, into english using the global translation dictionaries
        found at the head of the file

        :param:
            mode_names : string
            transport mode names
        :return:
            mode_names : string
        """
        if mode_names:
            mode_list = mode_names.split(',')
            translations = []
            for mode in mode_list:
                translations.append(MODE_TRANSLATIONS[mode.lstrip()])
            return str(translations).strip('[]').replace("'", '')
        else:
            return mode_names

def make_translations(data):
        """
        translates the columns and fields of the data from French to English
        """
        if not 'car' in data['mode'].unique():
            data['mode'] = data['mode'].apply(mode_to_new_name)
        if not 'work' in data['purpose'].unique():
            data['purpose'] = data['purpose'].apply(lambda pur: PURPOSE_TRANSLATIONS[pur] if pur else pur)
        return data


def translate_data(filename):
    """
    Entry point to translate data
    """
    try:
        # utf-8 needed to read french letters
        data = gpd.read_file(filename, encoding='utf-8')
    except:
        print("path/to/filename not found")
        raise
    data = make_translations(data)
    return data
