from app import bp
from flask import Flask, render_template, request


def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    return 'ok'


def pagina_no_encontrada(error):
    return render_template('404.html'), 404


app = Flask(__name__)
app.secret_key = "ffgghhllmm"
app.register_blueprint(bp)
app.static_folder = 'app/static'
app.register_error_handler(404, pagina_no_encontrada)

if __name__ == '__main__':
    app.run(debug=True)
