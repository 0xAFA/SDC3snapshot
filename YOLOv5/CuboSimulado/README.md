# YOLOv5

Pasos para aplicar el modelo YOLOv5:

#### 1. Ajustar el formato de las imágenes y las anotaciones

Las imágenes se pueden dar en cualquier formato común (png, jpg, bmp, tiff). Usar si es posible el mismo formato para entrenamientoy evaluación. Si tenemos un cubo, obtener las imágenes individuales con astropy.

El formato de anotaciones es:
* archivo .txt, un archivo por imagen
* un objeto por línea
* cada línea son cinco números: categoría, x_center, y_center, width, height
* las categorías se identifican con números enteros. Si sólo tenemos una categoría de objetos, poner siempre 0
* las coordenadas son relativas al tamaño de la imagen (entre 0 y 1)

Ejemplo:

```
0 0.18359375 0.2734375 0.012494346893507932 0.012494346893507932
0 0.84375 0.30859375 0.01738557665279713 0.01738557665279713
0 0.81640625 0.66015625 0.010532732165151265 0.010532732165151265
0 0.662109375 0.787109375 0.016984596255208536 0.016984596255208536
0 0.966796875 0.638671875 0.0014424932451825704 0.0014424932451825704
```

#### 2. Dividir los datos en train y test

Separar las imágenes y etiquetas en tres carpetas: train, test y val, con las proporciones que queramos. El script train_test_split.py en esta carpeta reordena los archivos automáticamente.

#### 3. Crear archivos de configuración

- Crear archivo .yaml con los directorios de los archivos y los nombres de las clases:

```yml
train: ../../CuboSimulado/images/train/ 
val:  ../../CuboSimulado/images/val/
test: ../../CuboSimulado/images/test/

# number of classes
nc: 1

# class names
names: ["galaxia"]
```

- Los modelos están en la carpeta models, usar uno de los que vienen por defecto o crear uno nuevo
- Los hiperparámetros están en `data/hyp.scratch.yaml`

#### 4. Entorno virtual

La carpeta yolov5 es una copia del repositorio oficial. Entrar en ella e instalar las dependencias de YOLO en un entorno virtual:

```
cd yolov5
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install scikit-learn

# Para usarlo con Jupyter
pip install ipykernel ipywidgets
python -m ipykernel install --user --name=YOLOv5
```

#### 5. Entrenar el modelo

(Este paso requiere una GPU con CUDA)

Ejecutar este comando desde el directorio yolov5, ajustando los parámetros si es necesario:
`python train.py --img 640 --cfg yolov5s.yaml --hyp hyp.scratch.yaml --batch 32 --epochs 100 --data cubo-simulado.yaml --weights yolov5s.pt --workers 24 --name yolo_cubo_simulado`

En este caso nos avisa de que los resultados pueden no ser buenos porque muchas de las regiones etiquetadas son pequeñas, debería funcionar mejor con datos con más resolución.

Los resultados aparecen en la carpeta runs. Esto genera un archivo de pesos (weights/best.pt), que usaremos después para evaluación e inferencia, y un conjunto de estadísticas sobre el rendimiento del modelo.

#### 6. Aplicar el modelo

Este paso se puede hacer en CPU, pero es mucho más rápido en GPU. Pasar como `source` la carpeta con los archivos a los que queremos aplicar el modelo, y como `weights` el archivo de pesos generado en el entrenamiento.

```
python detect.py --source ../CuboSimulado/images/test/ --weights runs/train/yolo_cubo_simulado/weights/best.pt --conf 0.25 --name yolo_cubo_simulado
```

Los resultados están en runs/detect.