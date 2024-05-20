from pymongo import MongoClient
from pymongo.server_api import ServerApi

def connect_database():
    uri = "mongodb+srv://Bernat:1234@contaminacionbcn.tacpnks.mongodb.net/?retryWrites=true&w=majority&appName=ContaminacionBCN"
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        return client["Contaminación"], client
    
    except Exception as error:
        print(error)
        return None, None

def search_results(neighborhood, date):
    search_result = []
    db, client = connect_database()

    estacion_id = get_neighborhood_id(db, neighborhood)

    if estacion_id:
        info_calidad = db.CalidadAire.find({"ESTACIO": estacion_id, "DIA": date})

        for result in info_calidad:
            data = {}

            info_cont = db.Contaminantes.find_one({"Codi_Contaminant": result["CODI_CONTAMINANT"]})

            data["result"] = result["H12"]
            data["desc"] = info_cont["Desc_Contaminant"]
            data["uni"] = info_cont["Unitats"]

            search_result.append(data)

        for value in search_result:
            print(f"{value['desc']}: {value['result']} {value['uni']}")

        client.close()

        return search_result
    else:
        client.close()
        return None

def get_neighborhood_id(db, neighborhood):
    id_document = db.Estaciones.find_one({"Nom_barri": neighborhood})

    if id_document:
        return id_document.get("Estacio")
    else:
        return None

def get_neighborhood_list():
    neighborhood_list = []

    db, client = connect_database()

    neighborhoods = db.Estaciones.distinct("Nom_barri")

    for neighborhood in neighborhoods:
        neighborhood_list.append(neighborhood)
        print(neighborhood)

    client.close()

    return neighborhood_list