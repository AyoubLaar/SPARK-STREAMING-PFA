from keras.models import load_model

model_file = "model/model.keras"

def build_model():
    model = load_model(model_file)
    return model