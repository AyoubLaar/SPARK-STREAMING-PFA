from tensorflow.keras import layers, Model, Input

def build_model():
    inputs = Input(shape=(1,), dtype=tf.string)
    x = int_vectorize_layer(inputs)
    # Embedding layer
    x = layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=MAX_SEQUENCE_LENGTH)(x)
    # SpatialDropout1D layer
    x = layers.SpatialDropout1D(drop_lstm)(x)
    # Bidirectional LSTM layer
    x = layers.Bidirectional(layers.LSTM(units=32))(x)
    # Dropout layer
    x = layers.Dropout(drop_lstm)(x)
    # Dense layers
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dense(64, activation='relu')(x)
    x = layers.Dense(32, activation='relu')(x)
    # Output layer
    outputs = layers.Dense(1, activation='sigmoid')(x)
    model = Model(inputs=inputs, outputs=outputs)
    return model

def build_model():
    inputs = Input(shape=(MAX_SEQUENCE_LENGTH,))
    # Embedding layer
    x = layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=MAX_SEQUENCE_LENGTH)(inputs)
    # SpatialDropout1D layer
    x = layers.SpatialDropout1D(drop_lstm)(x)
    # Bidirectional LSTM layer
    x = layers.Bidirectional(layers.LSTM(units=32))(x)
    # Dropout layer
    x = layers.Dropout(drop_lstm)(x)
    # Dense layers
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dense(64, activation='relu')(x)
    x = layers.Dense(32, activation='relu')(x)
    # Output layer
    outputs = layers.Dense(1, activation='sigmoid')(x)
    model = Model(inputs=inputs, outputs=outputs)
    model.load_weights("model.weights.h5")
    return model