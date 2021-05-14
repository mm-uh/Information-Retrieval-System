# Proyecto de Sistemas de Información

El proyecto esta compuesto por dos partes el SRI que puede ejecutarse en una modalidad para evaluarse sobre una colección específica o como servicio web para utilizar la aplicación web Moogle.

En caso que desee instalar todas las dependencias del proyecto y cuenta con la herramienta make, npm y python, puede correr el siguiente comando:
```
make build-deps
```

## SRI

Para ejecutar el SRI debe tener instalado los paquetes

- flask
- flask_cors
- nltk

El programa recibe los siguientes flags mediante la línea de comandos:

- '-e' Si este flag es pasado al programa este se ejecutará en modo evaluación, que consiste en mostrar los valores obtenidos para las métricas Recobrado, Precisión y Medida F1 sobre la colección especificada. En caso de no usar este flag el programa iniciará como servicio web usando como base de conocimientos la colección indicada.
- '-c' Este flag debe ir acompañado de la colección a utilizar que puede ser Cransfield, Medline o Cisi. Si este flag no es especificado se utiliza por defecto la colección Cransfield.

## Moogle

Moogle es una aplicación web desarrollada utilizando el framework React, para ejecutarla solo se debe ejecutar en la carpeta los siguientes comandos:

- npm install
- npm start

Luego de iniciado debe abrir la aplicacion web desde donde puede realizar consultas.
