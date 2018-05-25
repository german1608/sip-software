from asignaturas.models import Asignatura
from coordinacion.models import Coordinacion

# Script para gestionar las asignaturas del sistema 
#       - Anadir
#       - Eliminar
#       - Modificar 

# Descripcion de la funcion 
#   - nombre: Nombre de la asignatura 
#   - codasig: Codigo de la asignatura 
#   - creditos: Numero de creditos de la asignatura 
#   - horario: Una lista de los atributos de horario 
#   - programa: una lista de los atributos de programa 
#   - coordinacion: una lista de los atributos de coordinacion 

def anadirAsignatura(nombre, codasig, creditos, horario, programa, coordinacion):

    # Agrego la informacion de la coordinacion a la cual 
    # pertenece la asignatura

    
    nombreCoord = coordinacion[0]
    codigo      = coordinacion[1]

    coordinacion = Coordinacion(nombre=nombreCoord, codigo=codigo)
    coordinacion.save()

    asignatura = Asignatura(nombre=nombre, codasig=codasig, creditos=creditos, pertenece=coordinacion)
    asignatura.save()

    # # Obtengo aqui la asignatura recien creada

    asignatura = Asignatura.objects.get(pk=codasig)

    # #------ Aqui se agrega el backend para agregar horarios a la materia -------#

    dia = horario[0]    
    hora_inicio = horario[1]
    hora_final = horario[2]

    asignatura.horarios.create(dia=dia, hora_inicio=hora_inicio, hora_final=hora_final)
    

    # #------ Aqui se agrega el backend para agregar los programas ---------------#

    codigoAs = programa

    asignatura.programas.create(codigo=codigoAs)

    

    print('Se agrego exitosamente la materia con el codigo: ' + asignatura.codasig)