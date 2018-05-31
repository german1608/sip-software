# Script para generar algunos objetos que perteneceran a la base de datos 

import datetime 
from asignaturas.models import Asignatura, Horario, ProgramaAsignatura
from profesores.models import Profesor
from coordinacion.models import Coordinacion

def is_empty(model):
    return (model.objects.all().count() == 0)


# Creacion de una coordinacion 


if is_empty(Coordinacion):
    coordinacion = Coordinacion(nombre="Computacion avanzada", codigo='12345')
    coordinacion.save()
else:   
    coordinacion = Coordinacion.objects.get(pk='12345')
    
# Creacion de las 5 asignaturas  
if is_empty(Asignatura):
    asignaturas = [ 
        Asignatura(nombre="Introduccion a la computacion avanzada", codasig="CI4715", creditos=5),
        Asignatura(nombre="Teoria de la computacion", codasig="CI1231",creditos=4),
        Asignatura(nombre="Matematicas combinatorias", codasig="MA3512", creditos=4),
        Asignatura(nombre="Mecanica avanzada", codasig="ME1234",creditos=3),
        Asignatura(nombre="Guerra fria, rock and roll y su impacto social", codasig="CS2345",creditos=4),
    ]

    # for asignatura in asignaturas:
    #     asignatura.save()
    #     print('Se agrego la asignatura con el codigo: ' + asignatura.codasig + ' a la base de datos')   

    for asignatura in asignaturas:
        coordinacion.asignaturas.create(nombre=asignatura.nombre, codasig=asignatura.codasig, creditos=asignatura.creditos) 

# Creacion de 5 profesores 

if is_empty(Profesor):
    profesores = [
        Profesor(primer_nombre='Sarah', primer_apellido='Elliot', cedula='562726925', carnet='11-10456', fecha_nacimiento=datetime.datetime(1997, 5, 27)),
        Profesor(primer_nombre='Wohehiv', segundo_nombre='Cholesky', primer_apellido='Henry', cedula='89616548', carnet='08-98565', fecha_nacimiento=datetime.datetime(1993, 3, 1)),
        Profesor(primer_nombre='Anguo', segundo_nombre='Larry', primer_apellido='Voong', cedula='99498489', carnet='09-11456', fecha_nacimiento=datetime.datetime(1996, 12, 30)),
        Profesor(primer_nombre='Munny', segundo_nombre='Jose', primer_apellido='Saelee', cedula='78464512', carnet='14-10254', fecha_nacimiento=datetime.datetime(1989, 2, 25)),
        Profesor(primer_nombre='Shaun', segundo_nombre='Diesel', primer_apellido='Reese', cedula='48646494', carnet='01-82556', fecha_nacimiento=datetime.datetime(1976, 7, 25)),
    ]

    for profesor in profesores:
        profesor.save()
        print('Se agrego exitosamente el profesor con el carnet: ' + profesor.carnet + ' a la base de datos')

# Se crean dos horarios por asignaturas
if is_empty(Horario):
    horarios = [
        Horario(dia= 0, hora_inicio= 7, hora_final= 8),
        Horario(dia= 2, hora_inicio= 9, hora_final= 12),
        Horario(dia= 3, hora_inicio= 10, hora_final= 11),
        Horario(dia= 4, hora_inicio= 13, hora_final= 15),
        Horario(dia= 1, hora_inicio= 15, hora_final= 16),
        Horario(dia= 2, hora_inicio= 7, hora_final= 10),
        Horario(dia= 3, hora_inicio= 8, hora_final=10),
        Horario(dia= 4, hora_inicio= 7, hora_final= 9),
        Horario(dia= 4, hora_inicio= 9, hora_final= 12),
        Horario(dia= 2, hora_inicio= 16, hora_final= 17),
    ]

    # En esta parte se agregan los horarios 
    iteradorHorarios = 0
    for asignatura in coordinacion.asignaturas.all():
        asignatura.horarios.create(dia=horarios[iteradorHorarios].dia, hora_inicio=horarios[iteradorHorarios].hora_inicio, hora_final=horarios[iteradorHorarios].hora_final)
        asignatura.horarios.create(dia=horarios[iteradorHorarios + 1].dia, hora_inicio=horarios[iteradorHorarios + 1].hora_inicio, hora_final=horarios[iteradorHorarios + 1].hora_final)
        iteradorHorarios += 2
        print("Se agrego exitosamente los horarios a la materia: " + asignatura.codasig)

# Se crean los programas por asignaturas
if is_empty(ProgramaAsignatura):
    programas = [
        ProgramaAsignatura(url='google.com'),
        ProgramaAsignatura(url='german.com'),
        ProgramaAsignatura(url='youtube.com'),
        ProgramaAsignatura(url='gustavo.com'),
        ProgramaAsignatura(url='daniel.com'),
    ]

    # Aqui se itera sobre las asignaturas y se le agregan los programas
    # asociados

    iteradorProgramas = 0
    for asignatura in coordinacion.asignaturas.all():
        asignatura.programas.create(url=programas[iteradorProgramas].url)
        asignatura.programas.create(url=programas[iteradorProgramas + 1].url)
        iteradorProgramas += 2
        print("Se asocio exitosamente los programas de la asignatura: " + asignatura.codasig)
        