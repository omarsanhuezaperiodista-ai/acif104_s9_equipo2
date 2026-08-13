# Refinamiento de la arquitectura MLP 16-8

**Modelo seleccionado:** MLP_16_8_D030

El refinamiento confirmó la configuración previamente seleccionada. Las variaciones de Dropout 0.25 y 0.35 no produjeron una mejora suficiente en validación para justificar el cambio del modelo final.

Orden principal: menor loss de validación, mayor F1 y mayor AUC. Con diferencias máximas de 0.001 en los tres criterios, se favorecen las menores brechas absolutas train-validación.

| Modelo | Capas ocultas | Dropout | Learning rate | Parámetros | Épocas ejecutadas | Mejor época | Loss entrenamiento restaurado | Loss validación | Brecha loss val-train | Accuracy entrenamiento restaurado | Accuracy validación | Brecha accuracy train-val | Precision validación | Recall validación | F1 validación | AUC validación |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MLP_16_8_D035 | [16, 8] | 0.35 | 0.001000 | 289 | 138 | 128 | 0.022418 | 0.022896 | 0.000478 | 0.990991 | 0.985714 | 0.005277 | 1.000000 | 0.969697 | 0.984615 | 1.000000 |
| MLP_16_8_D030 | [16, 8] | 0.30 | 0.001000 | 289 | 126 | 116 | 0.023747 | 0.023691 | -0.000056 | 0.990991 | 0.985714 | 0.005277 | 1.000000 | 0.969697 | 0.984615 | 1.000000 |
| MLP_16_8_D025 | [16, 8] | 0.25 | 0.001000 | 289 | 117 | 107 | 0.024273 | 0.024794 | 0.000522 | 0.990991 | 0.985714 | 0.005277 | 1.000000 | 0.969697 | 0.984615 | 1.000000 |

La selección utilizó exclusivamente validación; el conjunto de prueba no fue utilizado para seleccionar Dropout.
