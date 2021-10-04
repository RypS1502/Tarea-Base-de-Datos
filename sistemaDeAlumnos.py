import pymongo
import os
print('Ejecutando el codigo, un momento por favor... (Tiempo de espera max 20s)')
client = pymongo.MongoClient("mongodb+srv://ryps:rypspassword@clustercertus.iyyf8.mongodb.net/test?retryWrites=true&w=majority")

db = client.test 

col = db.alumno
def menu():
    os.system('cls')
    print('''
    ******************************
    Sistema de registro de alumnos
    ******************************''')

    while(True):
        print('''\n¿Qué desea hacer?:
        1) Consulta de registro de alumnos
        2) Consultar alumnos por apellidos
        3) Actualizar registro
        4) Añadir alumno
        5) Borrar alumno
        6) Terminar Programa\n''')

        eleccion = input('Ingrese su elección: ')

        if eleccion == '1':
            registro()

        elif eleccion == '2':
            ap = input('Ingrese los apellidos a buscar: ')
            consultaAlumnosPorApellido(ap)

        elif eleccion == '3':
            actualizarRegistro()

        elif eleccion == '4':
            añadiralumno()

        elif eleccion == '5':
            ap = input('Ingrese los apellidos para seleccionar al alumno a eliminar: ')
            borrarAlumnoporApellido(ap)

        elif eleccion == '6':
            break

        else:
            print('--x--> Opcion inválida o desconocida, intente de nuevo.')


def registro():
    os.system('cls')
    registro =  col.find().sort('nombre', 1)

    print('------------------------------------------------------------------------------------------------')
    print('{:20} {:25} {:8} {:66}'.format('Nombre', 'Apellidos', 'Edad', 'Cursos'))
    print('------------------------------------------------------------------------------------------------')
    for alumno in registro:
        cursos = ''
        cont = 0
        for curso in alumno['cursos']:
            cont += 1
            cursos += curso
            if cont < len(alumno['cursos']):
                cursos += ', '
            else:
                cursos += '.'
        print('{:<20} {:<25} {:<8} {:<66}'.format(alumno['nombre'], alumno['apellidos'], alumno['edad'], cursos))

def consultaAlumnosPorApellido(ape):
    os.system('cls')
    consulta = col.find({
        'apellidos':ape
    }).limit(20)

    print('------------------------------------------------------------------------------------------------')
    print('{:20} {:25} {:8} {:66}'.format('Nombre', 'Apellidos', 'Edad', 'Cursos'))
    print('------------------------------------------------------------------------------------------------')
    for alumno in consulta:
        cursos = ''
        cont = 0
        for curso in alumno['cursos']:
            cont += 1
            cursos += curso
            if cont < len(alumno['cursos']):
                cursos += ', '
            else:
                cursos += '.'
        print('{:<20} {:<25} {:<8} {:<66}'.format(alumno['nombre'], alumno['apellidos'], alumno['edad'], cursos))
    
    if len(list(col.find({'apellidos':ape}))) == 0:
        print('Ninguna coincidencia encontrada.')

def actualizarRegistro():
    nom = input('Ingresa los nombres del alumno a actualizar: ')
    ape = input('Ingresa los apellidos del alumno a actualizar: ')
    consulta = col.find({
        'nombre':nom,
        'apellidos':ape
    })
    os.system('cls')
    if len(list(consulta)) == 1:
        print('''¿Qué desea hacer?
        1) Sobreescribir todos los datos del alumno
        2) Sobreescribir un dato del alumno''')
        option = input('Inserte su elección: ')
        os.system('cls')
        if option == '1':
            print('\nA continuación escriba los datos como desee modificarlos (se sobreescribiran):\n')
            nom1 = input('Escriba los nuevos nombres: ')
            ape1 = input('Escriba los nuevos apellidos: ')
            edad = input('Escriba la nueva edad: ')
            cursos = input('Ingrese los cursos separados por comas (,): ')

            misCursos = []
            for curso in cursos.split(','):
                misCursos.append(curso)
            print('Actualizando la información...')
            actualizar = col.update_one({
                'nombre':nom,
                'apellidos':ape
            },
            {
                '$set': {
                    'nombre': nom1,
                    'apellidos':ape1,
                    'edad': edad,
                    'cursos': misCursos
                }
            })
            os.system('cls')
            print('----> Se modificó ', actualizar.modified_count, ' registro de alumno.')
        elif option == '2':
            print('''Selecciona el dato que quieres actualizar:
                1) Nombres
                2) Apellidos
                3) Edad
                4) Cursos''')
            sel = input('Ingrese su elección: ')
            os.system('cls')
            if sel == '1':
                nom1 = input('Escriba los nuevos nombres: ')
                print('Actualizando la información...')

                col.update_one({
                    'nombre':nom,
                    'apellidos':ape
                },
                {
                    '$set': {
                                'nombre': nom1
                    }
                })
                os.system('cls')
                print('----> Se modificó los nombres del alumno.')
            elif sel == '2':
                ape1 = input('Escriba los nuevos apellidos: ')
                print('Actualizando la información...')

                col.update_one({
                    'nombre':nom,
                    'apellidos':ape
                },
                {
                    '$set': {
                                'apellidos':ape1,
                    }
                })
                os.system('cls')
                print('----> Se modificó los apellidos del alumno.')
            elif sel == '3':
                edad = input('Escriba la nueva edad: ')
                print('Actualizando la información...')

                col.update_one({
                    'nombre':nom,
                    'apellidos':ape
                },
                {
                    '$set': {
                        'edad': edad,
                    }
                })
                os.system('cls')
                print('----> Se modificó la edad del alumno.')
            elif sel == '4':
                cursos = input('Nota: se sobreescribirán | Ingrese los cursos separados por comas (,): ')

                misCursos = []
                for curso in cursos.split(','):
                    misCursos.append(curso)
                print('Actualizando la información...')
                col.update_one({
                    'nombre':nom,
                    'apellidos':ape
                },
                {
                    '$set': {
                        'cursos': misCursos
                    }
                })
                os.system('cls')
                print('----> Se modificaron los cursos del alumno.')
            else:
                print('--x--> Opcion inválida o desconocida, intente de nuevo.')
        else:
            print('--x--> Opcion inválida o desconocida, intente de nuevo.')


    elif len(list(consulta)) == 0:
        print('--x--> No se encontró el registro del alumno ingresado intente de nuevo.')

def añadiralumno():
    os.system('cls')
    unAlumno = {}
    misCursos = []

    print('''     Añadir Alumno al registro
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~''')
    nombre = input('Ingrese un nombre: ')
    apellidos = input('Ingrese los apellidos: ')
    edad = input('Ingrese la edad: ')
    cursos = input('Ingrese los cursos separados por comas (,): ')

    consulta = col.find({
        'nombre': nombre,
        'apellidos': apellidos
    })

    if len(list(consulta)) == 0:
        for curso in cursos.split(','):
            misCursos.append(curso)

        unAlumno['nombre'] = nombre
        unAlumno['apellidos'] = apellidos
        unAlumno['edad'] = edad
        unAlumno['cursos'] = misCursos

        print('Grabando la información...')
        dato = col.insert_one(unAlumno)

        os.system('cls')
        print('----> Id insertado: ', dato.inserted_id)

        for documento in col.find({
            '_id': {
                '$eq':dato.inserted_id
            }
        }):
            print(documento)
    else:
        os.system('cls')
        print('--|--> Ya existe un documento con los nombres y apellidos ingresados.')

def borrarAlumnoporApellido(ape):
    os.system('cls')
    res = col.find({
        'apellidos':ape
    })
    cont = len(list(res))
    if cont == 1:
        print('Borrando al alumno seleccionado...')
        res = col.delete_one({
            'apellidos':ape
        })
        os.system('cls')
        print('----> Se borró ', res.deleted_count, ' alumno del registro.')
    elif cont == 0:
        os.system('cls')
        print('--x--> No se encontró el alumno, intente de nuevo.')
    elif cont > 1:
        os.system('cls')
        print('--||--> Se encontraron 2 o mas alumnos con el mismo apellido.')
        nom = input('\nIngrese los nombres del alumno: ')
        res2 = col.find({
            'nombre':nom,
            'apellidos':ape
        })
        cont2 = len(list(res2))
        if cont2 == 0:
            os.system('cls')
            print('--x--> No se encontró el alumno, intente de nuevo.')
        elif cont2 == 1:
            print('Borrando al alumno seleccionado...')
            res2 = col.delete_one({
            'nombre':nom,
            'apellidos':ape
            })
            os.system('cls')
            print('----> Se borró ', res2.deleted_count, ' alumno del registro.')




#Principal
menu()