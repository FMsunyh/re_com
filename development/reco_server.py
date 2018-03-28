from server.algorithm.keras_retinanet.bin.predict import load_model
from server import app
from server.algorithm.utils import set_cpu

if __name__ == '__main__':
    set_cpu()
    load_model()
    app.run('0.0.0.0', 16888, debug=True, use_reloader=False)