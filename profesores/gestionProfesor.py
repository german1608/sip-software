
from profesores.models import Profesor
# En este script se encuentra las funciones para gestionar la tabla de 
# profesores 
#       - Anade (Por ahora solo esta funcion)
#       - Elimina 
#       - Modifica 

def anadirProfesor(nombres, apellidos, cedula, carnet, f_nacimiento):
    # Se crea un objeto profesor para almacenar la informacion entrante 
    profesorAgregar = Profesor(
        primer_nombre=nombres[0],
        segundo_nombre=nombres[1],
        primer_apellido=apellidos[0],
        segundo_apellido=apellidos[1],
        cedula=cedula,
        carnet=carnet,
        fecha_nacimiento=f_nacimiento
    )

    profesorAgregar.save()
    print('El profesor con carnet: ' + profesorAgregar.carnet + ' fue agregado exitosamente')

