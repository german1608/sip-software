# Script para generar algunos objetos que perteneceran a la base de datos 

import datetime 
from asignaturas.models import Asignatura, Horario, ProgramaAsignatura
from profesores.models import Profesor
from coordinacion.models import Coordinacion

def is_empty(model):
    return (model.objects.all().count() == 0)


# Creacion de una coordinacion 


if is_empty(Coordinacion):
    coordinacion = Coordinacion(nombre="MAESTRÍA EN CIENCIAS DE LA COMPUTACIÓN", codigo='12345')
    coordinacion.save()
else:   
    coordinacion = Coordinacion.objects.get(codigo='12345')


if is_empty(Profesor):
    profesores = [
        Profesor(primer_nombre='Jirafales', primer_apellido='García', cedula='562726925', carnet='01-10456', fecha_nacimiento=datetime.datetime(1981, 5, 27)),
    ]

    for profesor in profesores:
        profesor.save()
        print('Se agrego exitosamente el profesor con el carnet: ' + profesor.carnet + ' a la base de datos')

# Creacion de las 5 asignaturas  
if is_empty(Asignatura):
    profesor = Profesor.objects.get(cedula='562726925')
    asignaturas = [ 
        Asignatura(nombre="TEORÍA DE LA COMPUTACIÓN", codasig="CI-7541", creditos=4),
        Asignatura(nombre="MATEMÁTICAS DE LA COMPUTACIÓN", codasig="CI-7521",creditos=4),
        Asignatura(nombre="TEORÍA DE ALGORITMOS", codasig="CI-7621", creditos=4),
        Asignatura(nombre="INTRODUCCIÓN A LAS BASES DE DATOS LOGIC V", codasig="CI-5432",creditos=4),
        Asignatura(nombre="COMPUTACIÓN GRÁFICA", codasig="CI-5321",creditos=4),
        Asignatura(nombre="INTELIGENCIA ARTIFICAL DISTRIBUIDA", codasig="CI-6437",creditos=4),
        Asignatura(nombre="ANÁLISIS DE ALGORITMOS PARALELOS", codasig="CI-6622",creditos=4),
        Asignatura(nombre="PROGRAMACIÓN FUNCIONAL", codasig="CI-6642",creditos=4),
        Asignatura(nombre="OPTIMIZACIÓN NO LINEAL I", codasig="CO-5412",creditos=4),
        Asignatura(nombre="DISEÑO Y ANALISIS DE EXPERIMENTOS", codasig="CO-6315",creditos=4),
        Asignatura(nombre="PROCESAMIENTO EN TIEMPO REAL", codasig="EC-6742",creditos=3),
        Asignatura(nombre="TEORÍA DE JUEGOS Y DECIS. EN GRUPOS", codasig="MA6635",creditos=4),
        Asignatura(nombre="TEC.HEURÍSTICA EN INVESTG. DE OPER", codasig="PS-7118",creditos=4),        
        Asignatura(nombre="TÓPICOS ESPECIALES EN INGENIERÍA DE SOFTWARE", codasig="CI-6741",creditos=4),        
        Asignatura(nombre="TÓPICOS EN ESTADISTICA III", codasig="CO-6323",creditos=4),
        Asignatura(nombre="TRABAJO DE GRADO", codasig="TG-8528",creditos=8),
    ]

    # for asignatura in asignaturas:
    #     asignatura.save()
    #     print('Se agrego la asignatura con el codigo: ' + asignatura.codasig + ' a la base de datos')   

    for asignatura in asignaturas:
        coordinacion.asignaturas.create(nombre=asignatura.nombre, codasig=asignatura.codasig, creditos=asignatura.creditos) 
        asignatura = Asignatura.objects.get(codasig=asignatura.codasig)
        # asignatura.save()
        # asignatura.pertenece = coordinacion
        asignatura.profesores.add(profesor)
        asignatura.save()

# Creacion de 5 profesores 

# Se crean dos horarios por asignaturas
if is_empty(Horario):
    horarios = [
        Horario(dia= 1, hora_inicio= 3, hora_final= 4),
        Horario(dia= 3, hora_inicio= 3, hora_final= 4),
    ]

    # En esta parte se agregan los horarios 
    iteradorHorarios = 0
    for asignatura in coordinacion.asignaturas.all():
        asignatura.horarios.create(dia=horarios[iteradorHorarios].dia, hora_inicio=horarios[iteradorHorarios].hora_inicio, hora_final=horarios[iteradorHorarios].hora_final)
        asignatura.horarios.create(dia=horarios[iteradorHorarios + 1].dia, hora_inicio=horarios[iteradorHorarios + 1].hora_inicio, hora_final=horarios[iteradorHorarios + 1].hora_final)
        print("Se agrego exitosamente los horarios a la materia: " + asignatura.codasig)

# Se crean los programas por asignaturas
if is_empty(ProgramaAsignatura):
    programas = [
        ProgramaAsignatura(url='https://PROG-01.com')
    ]

    # Aqui se itera sobre las asignaturas y se le agregan los programas
    # asociados

    iteradorProgramas = 0
    for asignatura in coordinacion.asignaturas.all():
        asignatura.programas.create(url=programas[iteradorProgramas].url)
        print("Se asocio exitosamente los programas de la asignatura: " + asignatura.codasig)
        