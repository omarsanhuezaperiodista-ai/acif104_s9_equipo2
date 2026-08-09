# Comparación experimental de tres arquitecturas MLP

**Modelo seleccionado:** MLP_16_8

Orden: menor loss de validación, mayor F1 y mayor AUC. Si loss, F1 y AUC difieren como máximo en 0.001, se elige el modelo más simple.

| Modelo | Capas | Dropout | LR | Parámetros | Épocas | Mejor época | Val loss | Accuracy | Precision | Recall | F1 | AUC | Brecha loss (val-train) | Brecha accuracy (train-val) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MLP_16_8 | [16, 8] | 0.30 | 0.001000 | 289 | 126 | 116 | 0.023691 | 0.985714 | 1.000000 | 0.969697 | 0.984615 | 1.000000 | -0.000056 | 0.005277 |
| MLP_1_capa | [16] | 0.20 | 0.002000 | 161 | 127 | 117 | 0.028673 | 0.985714 | 1.000000 | 0.969697 | 0.984615 | 0.999181 | 0.007962 | 0.014286 |
| MLP_32_16 | [32, 16] | 0.40 | 0.000500 | 833 | 141 | 131 | 0.036272 | 0.985714 | 1.000000 | 0.969697 | 0.984615 | 0.999181 | 0.016890 | 0.014286 |

La selección utilizó únicamente el conjunto de validación; el conjunto de prueba quedó reservado para la evaluación final.
