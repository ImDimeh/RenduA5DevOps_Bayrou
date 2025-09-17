import azure.functions as func
import datetime
import json
import logging
import os
from azure.cosmos import CosmosClient, exceptions

app = func.FunctionApp()

@app.function_name(name="postVote")
@app.route(route="postVote", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
@app.cosmos_db_output(
    arg_name="outputDocument",
    connection="COSMOS_CONN_STRING",
    database_name="VoteDataDatabase",
    container_name="VoteDataID",
    create_if_not_exists=True
)
def post_vote(req: func.HttpRequest, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info("Processing POST /postVote")
    try:
        # Lire le JSON envoyé dans la requête
        body = req.get_json()
        nom = body.get("nom")
        prenom = body.get("prenom")
        mail = body.get("mail")
        resultat_vote = body.get("resultat_vote")
        

        # Vérification des champs requis
        if not all([nom, prenom, mail, resultat_vote]):
            return func.HttpResponse(
                json.dumps({"error": "Missing required fields: nom, prenom, mail, resultat_vote"}),
                mimetype="application/json",
                status_code=400
            )

        # Créer le document JSON
        document = {
            "id": mail,  # ID unique = mail (ou autre clé unique)
            "nom": nom,
            "prenom": prenom,
            "mail": mail,
            "resultat_vote": resultat_vote
        }

        # Écrire dans Cosmos DB
        outputDocument.set(func.Document.from_dict(document))

        return func.HttpResponse(
            json.dumps({"status": "saved", "document": document}),
            mimetype="application/json",
            status_code=201
        )

    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON in request body"}),
            mimetype="application/json",
            status_code=400
        )
    except Exception as e:
        logging.error(f"Erreur lors de lʼinsertion : {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )
    



# GET all votes
@app.function_name(name="getAllVotes")
@app.route(route="GetAllVoteData", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
@app.cosmos_db_input(
    arg_name="inputDocument",
    connection="COSMOS_CONN_STRING",        # défini dans local.settings.json ou App Settings Azure
    database_name="VoteDataDatabase",
    container_name="VoteDataID",
    sql_query="SELECT * FROM c"
)
def get_all_votes(req: func.HttpRequest, inputDocument: func.DocumentList) -> func.HttpResponse:
    logging.info("Processing GET /GetAllVoteData")
    
    logging.info(f"Documents received from Cosmos DB: {len(inputDocument)}")  # <-- ajout

    try:
        if inputDocument and len(inputDocument) > 0:
            # Convertir tous les documents en liste de dicts
            votes = [doc.to_dict() for doc in inputDocument]
            return func.HttpResponse(
                body=json.dumps({"status": "success", "votes": votes}),
                mimetype="application/json",
                status_code=200
            )
        else:
            return func.HttpResponse(
                json.dumps({"status": "success", "votes": []}),
                mimetype="application/json",
                status_code=200
            )
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des votes : {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )