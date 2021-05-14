# Informe SI

## Diseño del sistema

 Nuesto sistema de recuperación de información preprocesa un conjunto de documentos para crear una "base de conocimientos", luego de esto es capaz de recibir consultas que son preprocesadas y crea un ranking con el conjunto de documentos que conforman nuestra "base de conocimientos", lo que permite obtener los documentos más relevantes a la consulta realizada (Ver figura del esquema). (Insertar esquema del sistema). A continuación explicamos con más detalles cada uno de estos pasos.

### Preprocesamiento de consultas y documentos

 Tanto las consultas como los documentos son recibidas en nuestro sistema como cadenas de caracteres representando lenguaje natural. Las cadenas recibidas son primeramente tokenizadas para dividir estas en términos que serán candidatos a ser términos indexados en nuestro sistema (los términos indexados son los términos relevantes para nuestro sistema de recuperación de información).
 Las secuencias de términos obtenidas luego del proceso de tokenizado son lematizadas. La lematización es un proceso que permite para un término específico obtener su lema que por convenio es la forma que se acepta como representante de las distintas formas flexionadas en las que puede aparecer una palabra o término (durante la creación del proyecto también se tuvo en cuenta la utilización de un proceso parecido conocido como "stemming", se decidió mantener lematización ya que "stemming" usa una serie de heurísticas para eliminar los finales de algunos términos por lo que es común que elimine partes de la palabra que no se desean eliminar), cabe destacar que para aumentar la precisión de este proceso primero se realiza la asignación del POS-TAG a cada uno de los términos.
 La secuencia de términos lematizados obtenida del proceso anterior es sometida al filtrado de signos de puntuación y de las conocidas como "stopwords", se decide eliminar estas palabras de nuestra secuencias porque consideramos que por nuestra elección de modelo de recuperación de información estas no serían necesarias ya que este no considera el orden o relación entre las palabras y estas "stopwords" no nos aportarían practicamente ningún valor.
 Las consultas pasan por un proceso adicional que consiste en filtrar todos los términos que no se encontraron en ningún documento.

### Representación de los documentos

 Al terminar el preprocesamiento de nuestros documentos tenemos como resultado para cada documento una secuencia de términos, el conjunto de términos que aparecen en estas secuencias son el conjunto de términos indexados de nuestro modelo, cada uno de estos términos recibe un valor entero que será su identificador, estos valores van de 0 a N-1 donde N es la cardinalidad del conjunto de términos indexados. Cada documento es representado en nuestro modelo por un vector de tamaño N. En la componente i del vector que representa a un documento se encuentra un valor real que determina el peso que tiene el término con identificador i en este documento, este peso es calculado multiplicando los valores de tf e idf del término.

### Representación de las consultas

Las consultas son representadas de la misma forma en que son representados los documentos, con la diferencia de que para calcular el valor de cada componente del vector se le aplica un suavizado al tf para amortiguar las grandes variaciones que ocurren en los pesos de los términos que ocurren poco en la consulta.

### Proceso de selección de documentos relevantes

Elaboramos nuestro sistema pensando en un escenario donde se quiere crear un SRI para dada una consulta sobre un tema determinado retornar documentos que contengan la respuesta o información sobre esta, los usuarios pensados no son expertos en el dominio del tema pero si poseen conocimientos sobre los vocablos y conceptos más importantes del dominio. Decidimos implementar un modelo clásico vectorial ya que este permite procesar consultas en lenguaje natural; los vectores que representan a los documentos son reales lo que permite diferenciar documentos conformados por el mismo conjunto de términos indexados; la puntuación otorgada a un documento para una consulta determinada es también real lo que permite detectar correspondencias parciales entre los documentos y la consulta solventando así que el usuario haya podido olvidar o confundir algún término de su consulta. Cuando nuestro sistema recibe una consulta esta es procesada hasta obtener el vector que la representa, luego se busca el coseno del ángulo entre el vector de la consulta y cada uno de los vectores que representan a los documentos de nuestra base de conocimientos, este valor es interpretado como la similitud entre la consulta y el documento y es el valor usado para crear el ranking de documentos del cual seleccionaremos los 10 documentos con mejor posición en este ranking, estos documentos serán los documentos mostrados al usuario como relevantes.

### Retroalimentación

Nuestro sistema posee un mecanismo de retroalimentación. El usuario es capaz de además de la consulta ingresar al sistema un conjunto de documentos relevantes y un conjunto de documentos no relevantes,  nuestro sistema usando la fórmula de Rocchio es capaz de crear un nuevo vector desplazando el vector original representante de la consulta en una dirección que lo acerque al centroide de los documentos relevantes y lo aleje del centroide de los documentos no relevantes. La fórmula de Rocchio posee 3 valores que definen el peso otorgado a la consulta, el peso otorgado a los documentos relevantes y el peso otorgado a los documentos no relevantes, nuestro sistema por defecto utiliza los valores 1, 0.9 y 0.3 respectivamente, aunque estos estan parametrizados y pueden ser cambiados; seleccionamos estos valores porque queremos que la consulta del usuario no pierda valor y queremos potenciar la selección de documentos relevantes, pero no queremos descartar todos los elementos no seleccionados como relevantes ya que puede ser que el usuario no los haya analizado todos detenidamente.

### Interacción con nuestro sistema

Nuestro sistema expone su utilización a través de un servicio web que es consumido por nuestra aplicación web Moogle. (foto de la pagina). El usuario es capaz de introducir una consulta en la barra de búsqueda y obtendrá un maximo de 10 documentos ordenados por nuestro sistema de ranking, cada documento es representado por su título y por las 250 palabras de su abstract. Luego de cada consulta el usuario puede seleccionar el conjunto de documentos que le parecieron relevantes y realizar nuevamente la consulta, (también puede realizar una consulta totalmente diferente pero debe tener en cuenta que la selección de documentos relevantes actual afectará su consula). (foto seleccionando documentos)

## Aspectos más importantes de la implementación del modelo

### Representación de conjuntos de datos

Los conjuntos de documentos y consultas son representados mediante una clase llamada Collection, lo importante sobre esta clase es que debe ser Iterable y los elementos que devuelva el iterador deben tener implementado el metodo __str__.

### Parsing del conjunto de documentos

Todos los datasets empleados para la evaluación de nuestro modelo tienen un formato como el de la conocida colección "Cranfield" por lo que se creó un parser para estos, este parser es expuesto en forma de una clase estática llamada CransfieldLikeParser la cual contiene una función parse que recibe el path al fichero que contiene los datos y devuelve un objeto de tipo Collection.

### Preprocesamiento

Para el procesamiento de los documentos y consultas utilizamos la libreria NLTK, de esta usamos el tokenizer, el conjunto de "stopwords", el lematizador y el POS tagger. La utilización de estas herramientas es realizada en la función preprocess_data la cual recibe un string representando el documento o consulta y retorna una lista de strings que es la secuencia de términos obtenidos.

### Index

La clase Index es una implentación de un índice invertido, el cual recibe un objeto de tipo Collection en su constructor representando los documentos a indexar y crea un objeto que ofrece, entre otros, los siguientes métodos que son utilizados principalmente en el cálculo de tf e idf:

- get_number_of_documents_with_word -> Este método recibe un término como entrada y retorna un entero significando la cantidad de documentos de la colección donde aparece este término.
- get_most_repeated_word_document -> Este método recibe el índice de uno de los documentos en la colección y devuelve un entero indicando la frecuencua del término con mayor frecuencia en el documento indicado.
- filter_non_indexed_words -> Este método recibe una secuencia de términos y devuelve una secuencia donde solo están los términos de la secuencia entrante que pertenecen al conjunto de términos indexados.
- get_posting -> Este método recibe un término y el índice de un documento y devuelve un objeto de tipo Posting (la clase Posting representa información sobre la ocurrencia de un término determinado en un documentos específico, nos permite conocer la frecuencia de un término determinado en un documento).

### VectorSpaceModel

VectorSpaceModel es una clase primordial en nuestro proyecto, aglutina todos los procesos explicados anteriormente. El constructor recibe un objeto de tipo Collection reprsentando los documentos de la base de conocimientos y recibe también una serie de parámetros que permiten modificar un poco el comportamiento del modelo, estos parámetros son la cantidad de documentos que se consideran relevantes a una consulta y los pesos utilizados en la fórmula de Rocchio. Esta clase solo expone el método query como su interfaz, pero contiene varios métodos útiles que consideramos importante mencionar:

- query -> Este método recibe la consulta en lenguaje natural y opcionalmente una lista de índices representando a los documentos relevantes y otra lista a los documentos irrelevantes. El método retorna una lista de enteros que son los índices en la colección de los documentos considerados relevantes.
- __create_query_vector -> Este método es el encargado de tomar la consulta en lenguaje natural y procesarla para obtener el vector que la representa, el método recibe las listas de documentos relevantes e irrelevantes porque en este el vector resultante se obtienen usando la formula de Rocchio, si ambas listas son vacías el vector resultante es solo la representación de la consulta directamente.
- __create_document_vector -> Este método recibe el índice de un documento en la colección de documentos y devuelve el vector que representa a este documento en nuestro espacio vectorial, este método es aplicado a todos los documentos en el constructor de la clase para evitar este cómputo en cada consulta.

En este módulo se encuentran también algunos metodos útiles como load_model y save_model que durante el proyecto nos evitaron el recómputo de los modelos cada vez que fueramos a utilizarlo, se adjuntan en el proyecto 3 modelos precomputados sobre las colecciones "Cransfield", "Cisi" y "Medline".

### Evaluator

Esta clase representa una interfaz que nos permite realizar ciertas evaluaciones sobre los modelos. Creamos dos clases que implementaran esta interfaz, SimpleEvaluator y FeedbackEvaluator, la primera evaluaba nuestro modelo con consultas y el segundo proveía retroalimentación a nuestro modelo. Para evaluar el comportamiento del modelo utilizamos 3 métricas: Recobrado, Precisión y Medida F1, más adelante abordaremos los resultados obtenidos en estas evaluaciones.

## Evaluación del modelo

Para evaluar el modelo se utilizaron dos colecciones "Cransfield" y "Medline", la primera es una recopilación de documentos sobre el tema aeronaútica y el segundo una recopilación de documentos sobre medicina. La colección "Cransfield" cuenta con un total de 1400 documentos y "Medline" con un total 1083 documentos.

### Medidas objetivas

Evaluamos el modelo respecto a 3 medidas objetivas estudiadas en clase: Recobrado, Precisión y Medida F1, a continuación vemos una tabla con la comparación de estas

Coleccion | Recobrado | Precisión | Medida F1
--- | --- | --- | ---
Cransfield  | 0.36 | 0.24 | 0.27
Medline (recuperando 10 documentos)| 0.29 | 0.59 | 0.38
Medline (recuperando 20 documentos)| 0.45 | 0.47 | 0.44

(fotos con ejemplos)

De aquí podemos ver que en ambas colecciones se recuperan alrededor de la tercera parte de documentos relevantes en cada consulta como promedio cuando devolvemos 10 documentos y cerca de la mitad usando "Medline" y devolviendo 20 documentos. La métrica precisión es la que mayor diferencia muestra teniendo que en la colección "Cransfield" solo un cuarto de los documentos recuperados son relevantes mientras que cerca de la mitad de los documentos recuperados en "Medline" son relevantes. Si utilizamos la Medida F1 como métrica "juez" podemos definir que nuestro modelo se comporta mejor sobre la colección "Medline" que sobre la colección "Cransfield", es necesario tener en cuenta que la cantidad de consultas realizadas sobre la colección "Medline" fue mucho menor.

### Medidas subjetivas

Consideramos que con ambas colecciones percibimos los mismos resultados en cuanto a:

- Tiempo de respuesta: Las respuestas son entregadas al usuario instantaneamente independientemente de la colección que se este usando, debemos tener en cuenta que ambas colecciones son bastante pequeñas en tamaño, en cualquier caso nuestro modelo se comporta lineal en cuanto a la cantidad de documentos a la hora de obtener las similitudes, luego ordena las similitudes introduciendo una complejidad NlogN por lo que consideramos que mientras los vectores de los documentos puedan mantenerse en la memoria RAM del dispositivo el modelo se comportará bien con colecciones más grandes. Cabe destacar que el NlogN introducido por el ordenamiento del ranking puede ser reducido a N*C donde C es la constante que indica cuantos documentos son devueltos por el modelo.

- Forma de presentación: Los documentos son devueltos en una lista donde se observa el título del documento y los primeros 250 caracteres del abstract como se pudo observar en las fotos anteriores, consideramos que es muy sencillo para el usuario a partir de aquí llegar al documento.

## Análisis de ventajas y desventajas

Nuestro sistema es capaz de recibir consultas en lenguaje natural; retorna resultados de forma instantanea; la correspondecia entre la consulta y los documentos recuperados no debe ser total por lo que otorga flexibilidad al usuario en el momento de realizar la consulta. Como principal desventaja del modelo observamos que no se tiene en cuenta la relación entre términos, ni se analizan términos en la consulta que no hayan sido previamente indexados, lo que evita aprovechar los contextos para dar resultados más eficaces; como observamos la correspondecia entre la consulta y los documentos es parcial y aunque esto lo vemos como una ventaja para el usuario también debemos mencionar que esto puede disminuir la precisión del modelo.

## Recomendaciones para mejorar el sistema

Usar un modelo de tipo "Espacio Vectorial Generalizado" que tienen en cuenta relaciones entre términos. Utilizar expansión de consultas para entre otras cosas proponer variantes a términos que no hayan sido previamente indexados.

