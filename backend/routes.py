from backend import backend

@backend.route('/')
@backend.route('/index')
def index():
    return('Hello Atulya!')