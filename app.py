from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Inicializar la lista de inscritos en sesión
@app.before_request
def iniciar_lista():
    if 'inscritos' not in session:
        session['inscritos'] = []

@app.route('/')
def registro():
    return render_template('registro.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    fecha = request.form.get('fecha')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    turno = request.form.get('turno')
    seminarios = request.form.getlist('seminarios')

    # Almacenar el nuevo inscrito como un diccionario
    inscrito = {
        'fecha': fecha,
        'nombre': nombre,
        'apellido': apellido,
        'turno': turno,
        'seminarios': ', '.join(seminarios)
    }

    # Guardar en la sesión
    session['inscritos'].append(inscrito)
    session.modified = True

    return redirect(url_for('lista_inscritos'))

@app.route('/lista')
def lista_inscritos():
    inscritos = session.get('inscritos', [])
    return render_template('lista_inscritos.html', inscritos=inscritos)

@app.route('/eliminar/<int:index>')
def eliminar(index):
    session['inscritos'].pop(index)
    session.modified = True
    return redirect(url_for('lista_inscritos'))

@app.route('/editar/<int:index>', methods=['GET', 'POST'])
def editar(index):
    if request.method == 'POST':
        # Actualizar el inscrito con los nuevos datos
        session['inscritos'][index]['fecha'] = request.form.get('fecha')
        session['inscritos'][index]['nombre'] = request.form.get('nombre')
        session['inscritos'][index]['apellido'] = request.form.get('apellido')
        session['inscritos'][index]['turno'] = request.form.get('turno')
        session['inscritos'][index]['seminarios'] = ', '.join(request.form.getlist('seminarios'))
        session.modified = True
        return redirect(url_for('lista_inscritos'))
    
    # Prellenar los datos actuales en el formulario de edición
    inscrito = session['inscritos'][index]
    return render_template('editar_inscrito.html', inscrito=inscrito, index=index)

if __name__ == '__main__':
    app.run(debug=True)
