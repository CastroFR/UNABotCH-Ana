import random
import json

import torch

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Ana UNABOT"

context = {}

def log_unknown_question(question):
    with open("unknown_questions.txt", "a", encoding="utf-8") as f:
        f.write(question + "\n")

def handle_follow_up(msg, context):
    if context.get('pending') == 'costos':
        carrera = msg.strip().lower()
        context.clear()
        return f"Los costos para {carrera.title()} son: <br>Matrícula: $500 <br>Mensualidad: $300 <br><a href='...'>Ver detalles</a>"
    return None

def extract_carrera(msg):
    # Lógica simple para detectar carreras
    carreras = ["enfermeria", "sistemas", "derecho", "agronomia"]
    
    for carrera in carreras:
        if carrera in msg.lower():
            return carrera
    return "esta carrera"

def get_response(msg):
    global context

     # Manejar seguimiento
    if context.get("pending"):
        #return handle_follow_up(msg, context)
        response = handle_follow_up(msg, context)
        if response: 
            return response
        
    # procesamiento inicial del mensaje    
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device, dtype=torch.float32)

    # predicción del modelo
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    # logica de respuesta
    response = "No comprendo..."

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                # Manejar respuesta
                response = random.choice(intent['responses'])

                if "%carrera%" in response:
                    carrera = extract_carrera(msg)
                    response = response.replace("%carrera%", carrera)

                # Establecer contexto si es necesario
                if tag == "costos":
                    context["pending"] = "costos"
                    return "¿Para qué carrera específica necesita información de costos?"
                
                return response
            
    # manejo de fallback
        if prob.item() < 0.65:
            log_unknown_question(msg)  # Registrar pregunta no reconocida
            return "Aún no sé responder eso, pero lo agregaré a mi entrenamiento. ¿Necesitas otra cosa?"
        # Mejorar el fallback
        else:
            return random.choice([
                "¿Necesitas ayuda con admisiones, becas u otro tema?",
                "Reformula tu pregunta. Temas disponibles: pensum, costos, horarios."
            ])
        return response
        #return "No comprendo..."
    return response



if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        #resp = get_response(sentence)
        #print(resp)

        print("Bot:", get_response(sentence))