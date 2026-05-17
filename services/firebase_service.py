import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from firebase_admin import auth

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

cred_path = os.path.join(
    BASE_DIR,
    "Firebase",
    "Firebase_Key.json"
)

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()


def criar_usuario(nome, email, senha):
    user = auth.create_user(
        email=email,
        password=senha
    )

    db.collection("usuarios").document(user.uid).set({
        "nome": nome,
        "email": email,
        "senha": senha
    })

    return user.uid