from .models import Asignatura
# En este script se encuentra las funciones para gestionar la tabla de 
# profesores 
#       - Anade 
#       - Elimina 
#       - Modifica 

def eliminarAsignatura(codasig):
    try:
        delete_return = Asignatura.objects.get(codasig=codasig).delete()
        print('Se borraron {} asignaturas: {}'.format(delete_return[0], delete_return[1]))
    except DoesNotExist as e:
        print(e)