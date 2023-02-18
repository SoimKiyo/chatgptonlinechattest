import asyncio
import websockets

# Crée une liste pour stocker les connexions utilisateur
users = {}

# Définit la fonction de gestion des messages entrants
async def message_handler(websocket, path):
    # Demande à l'utilisateur de saisir un pseudonyme et l'ajoute à la liste des utilisateurs connectés
    await websocket.send("Veuillez entrer un pseudonyme :")
    pseudonyme = await websocket.recv()
    users[websocket] = pseudonyme
    print(f"{pseudonyme} s'est connecté")

    try:
        async for message in websocket:
            print(f"Message reçu : {users[websocket]}: {message}")
            # Transmet le message à tous les utilisateurs connectés
            tasks = [user.send(users[websocket] + ": " + message) for user in users if user.open]
            if tasks:
                await asyncio.gather(*tasks)
            else:
                # S'il n'y a aucun utilisateur connecté, ferme la connexion
                await websocket.close()
                print(f"Connexion fermée pour {pseudonyme}")
                return
    finally:
        # Supprime la connexion utilisateur de la liste des utilisateurs connectés
        del users[websocket]
        print(f"{pseudonyme} s'est déconnecté")

# Crée un serveur websockets
start_server = websockets.serve(message_handler, 'https://chatgpttestcomm.onrender.com/', 8766)
print("IP:",start_server)

# Démarre le serveur
asyncio.get_event_loop().run_until_complete(start_server)

# Boucle infinie pour attendre les connexions utilisateur
asyncio.get_event_loop().run_forever()
