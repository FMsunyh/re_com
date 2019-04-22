from server import app
from server.algorithm.utils import set_cpu

if __name__ == '__main__':
    # set_cpu()
    app.run('0.0.0.0', 26888)