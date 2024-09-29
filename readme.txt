ARCHIVOS DEL PROYECTO, FUNCIÓN Y EXPLICACIÓN DE CÓDIGO

------------------------------------------------------------------------------------------------------------------------------

main.py: Este es el punto de inicio del programa. Aquí se gestionarán las interacciones del usuario, como la generación de nuevas claves y el almacenamiento.

	QApplication(sys.argv):
		- QApplication: Es la clase que gestiona el ciclo de eventos de la aplicación y, por lo tanto, es el núcleo de cualquier programa en 
		  PyQt6.
		- sys.argv: Es una lista que contiene los argumentos de línea de comandos que fueron utilizados para ejecutar el programa.

    Al pasar sys.argv a QApplication, la aplicación puede procesar los argumentos de la línea de comandos. Aunque muchas veces no hay argumentos específicos para 
    procesar, es buena práctica incluirlo por si alguna vez los necesito.
    Si no hay ningún argumento importante para pasar, simplemente paso una lista vacía [].
    Esta línea crea una instancia de QApplication, que es esencialmente el motor que hará que la interfaz gráfica funcione.

	window = PasswordManager():
		- Aquí, se está creando una instancia de la clase PasswordManager, que es la ventana principal. Esta clase es una subclase de 
		  QMainWindow (o puede heredar de otra clase de ventana) que contiene la interfaz gráfica del programa, con todos sus widgets y 
		  lógica de la interfaz.
		- Esta línea inicializa la ventana principal de la aplicación, que fue definida en la clase PasswordManager.

	window.show():
		- Este método le dice a PyQt6 que muestre la ventana en pantalla.
		- Sin show(), la ventana se crea pero no se renderiza en la pantalla, lo que significa que no sería visible para el usuario.

	sys.exit(app.exec()):
		- app.exec(): Aquí es donde empieza el ciclo de eventos de la aplicación. Este método entra en un bucle que gestiona todas las 
		  interacciones de la interfaz gráfica (como los clics de botones, la interacción con el teclado, etc.). Mientras este bucle se está 
		  ejecutando, la aplicación está "viva" y responde a los eventos del usuario. Cuando se cierra la ventana o se llama explícitamente a 
		  app.quit(), el ciclo de eventos termina y el programa finaliza.
		- sys.exit(): Esta función asegura que la aplicación cierre correctamente devolviendo un código de salida. El código de salida de la 
		  aplicación es importante, ya que indica si el programa terminó correctamente o si hubo algún error.
		  app.exec() devuelve un código de estado (generalmente 0, si todo está bien), y sys.exit() se asegura de que este valor se devuelva 
		  al sistema operativo.
 		  Esta línea inicia el ciclo de eventos de la aplicación y asegura que el programa se cierre correctamente cuando el ciclo de eventos 
		  termina.


gui/interface.py: aquí se concentra todo lo relacionado a la interfaz gráfica de la aplicación.
	Al especificar self como segundo argumento, PyQt6 entiende que este botón debe "vivir" dentro de la ventana principal (PasswordManager). Esto tiene varios 
        efectos:
		- El botón será mostrado en la ventana.
		- La gestión de memoria del botón está vinculada al objeto self. Si la ventana es cerrada o destruida, el botón también lo será automáticamente.
		- La posición y el comportamiento del botón serán relativos a su ventana padre.
    
    QVBoxLayout(): Es un layout (diseño o esquema) que organiza los widgets verticalmente, uno debajo del otro. 
                   En PyQt6, los layouts se utilizan para controlar cómo se distribuyen y organizan los widgets dentro de una ventana.
    
    QWidget(): Es un widget genérico que sirve como contenedor para otros widgets y layouts. En este caso, se crea un contenedor 
               que va a envolver todos los widgets organizados dentro del layout.

    setLayout(layout): Este método asigna el layout creado anteriormente al contenedor (container). Esto hace que el contenedor use 
                       ese layout para colocar los widgets.



utils/password_utils.py: Contiene las funciones para generar contraseñas que cumplan con los requisitos (mayúsculas, números, caracteres especiales) y realizar sustituciones.
	
	random.choices():
		- random.choices(population, k) selecciona k elementos de forma aleatoria de la secuencia population. A diferencia de random.choice(),
		  que selecciona solo un elemento, random.choices() puede devolver varios elementos.
		- En este caso, la función está eligiendo 2 letras mayúsculas al azar de la secuencia string.ascii_uppercase. El parámetro k=2 indica 
		  que se seleccionarán exactamente dos letras.

	random.shuffle(all_characters):
		- Esta función toma la lista all_characters (que contiene los caracteres de la clave generada) y mezcla sus elementos de manera aleatoria.
		- Sin embargo, después de mezclarla, all_characters sigue siendo una lista de caracteres.
		- El método ''.join() toma un iterable (como una lista o tupla) y une todos sus elementos en una sola cadena de texto, utilizando el 
		  string que aparece antes del .join() como separador. En este caso, el separador es una cadena vacía '', por lo que simplemente une 
		  todos los elementos de la lista sin espacios ni otros caracteres entre ellos.
	
	    Por ejemplo, si all_characters es: ['A', 'b', '1', '#', 'C', '9', 'e', '@']
	    El resultado de ''.join(all_characters) sería: "Ab1#C9e@"	


storage/db_manager.py: Aquí se gestiona cómo y dónde se guardan y recuperan las contraseñas en la BD.

tasks/scheduler.py: Se encargará de automatizar la notificación de claves a vencer cada 6 meses, a partir de la fecha de creación de la clave. 
