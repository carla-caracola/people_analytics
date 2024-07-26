# CONCLUSIONES

- Todas las columnas que contienen valores nulos son de tipo `object`.

## Columnas y su tipo de variable

### Variables Numéricas

- **`Age`**: Variable numérica discreta. Cambiar valores por extenso a numérico y tipo de la columna a `int64`. Crear columna nueva que categorice rangos de edad.

- **`DailyRate`**: Variable numérica continua. Se debe eliminar el símbolo `$` y convertir el tipo de datos a `float64`. Incluye valores numéricos decimales pero aparece como columna de tipo string. Deberás hacer los cambios necesarios para convertirla en columna de tipo numérica. Analizar la calidad de datos en comparación con las demás variables similares: `HourlyRate`, `MonthlyIncome`, `MonthlyRate`.

- **`DistanceFromHome`**: Variable numérica discreta. No hay valores faltantes. Tiene 192 valores negativos. Los valores negativos podemos pasarlos a positivos, confirmado por César.

- **`HourlyRate`**: Variable numérica continua sin valores faltantes. 84 valores = "Not Available". Cambiar el tipo de datos a `float` y corregir "Not Available" para que sean `Null`.

- **`MonthlyIncome`**: Variable numérica continua con un 52% de valores faltantes. Cambiar tipo a `float64` y comas por puntos.

- **`MonthlyRate`**: Variable numérica continua sin valores faltantes.

- **`NUMCOMPANIESWORKED`**: Variable numérica discreta sin valores faltantes, valores de 0-9.

- **`PercentSalaryHike`**: Variable numérica continua sin valores faltantes.

- **`PerformanceRating`**: Variable numérica discreta con 12% de valores faltantes. Cambiar tipo a `int64`.

- **`TOTALWORKINGYEARS`**: Variable numérica discreta con un 32% de valores faltantes. Cambiar tipo a `int64`.

- **`TrainingTimesLastYear`**: Variable numérica discreta sin datos faltantes.

- **`YearsAtCompany`**: Variable numérica discreta sin datos faltantes.

- **`YearsInCurrentRole`**: Variable numérica discreta con un 98% de valores faltantes.

- **`YearsSinceLastPromotion`**: Variable numérica discreta sin datos faltantes.

- **`YEARSWITHCURRMANAGER`**: Variable numérica discreta sin datos faltantes.

- **`DateBirth`**: Variable numérica de intervalo (año de nacimiento) sin valores faltantes.

### Variables Categóricas

- **`Attrition`**: Variable categórica binaria. Es un valor histórico, no conocemos el periodo en el que está contabilizado ni el/los tipos de rotaciones que contempla (consultado con el PO, César).

- **`BusinessTravel`**: Variable categórica nominal con un 48% de valores nulos. Utilizar en el análisis de forma segmentada, excluyendo registros nulos.

- **`Department`**: Variable categórica nominal con un 81% de valores nulos. Rellenar datos faltantes a partir de la columna `JobRole` si es posible.

- **`Education`**: Variable categórica ordinal sin valores faltantes, con valores del 1 al 5.

- **`EducationField`**: Variable categórica nominal, 6 valores únicos con un 46% de valores nulos.

- **`employeenumber`**: Variable categórica nominal. Identificador único para cada empleado, pero con duplicados que deben ser analizados.

- **`EnvironmentSatisfaction`**: Variable categórica ordinal sin valores faltantes. Transformar valores que superan 4 a nulos y desestimarlos en los cálculos.

- **`Gender`**: Variable categórica nominal binaria sin valores faltantes. Reemplazar por "Male" y "Female".

- **`JobInvolvement`**: Variable categórica ordinal sin valores faltantes. Cambiar tipo a `object`.

- **`JobLevel`**: Variable categórica ordinal sin valores faltantes. Cambiar tipo a `object`.

- **`JobRole`**: Variable categórica nominal sin valores faltantes. Corregir valores: hacer strip y corregir errores tipográficos.

- **`JobSatisfaction`**: Variable categórica ordinal sin valores faltantes. Tiene valores únicos del 1 al 4. Mantener.

- **`MaritalStatus`**: Variable categórica nominal con un 40% de valores faltantes. Corregir errores tipográficos.

- **`Over18`**: Variable categórica binaria con 56% de valores faltantes. Valores "Y" y `NaN`.

- **`OverTime`**: Variable categórica binaria con 42% de valores faltantes. Valores "No", `NaN`, y "Yes".

- **`RelationshipSatisfaction`**: Variable categórica ordinal sin valores faltantes. Tiene valores únicos del 1 al 4. Mantener.

- **`StockOptionLevel`**: Variable categórica ordinal sin valores faltantes.

- **`WORKLIFEBALANCE`**: Variable categórica ordinal con un 7% de valores faltantes. Cambiar tipo a `int64`.

- **`RemoteWork`**: Variable categórica binaria sin valores faltantes. Normalizar los valores.

### Variables a Eliminar

- **`employeecount`**: Variable constante sin valores faltantes, todos los valores son iguales a 1. No aporta valor. Remover esta columna.

- **`SameAsMonthlyIncome`**: Eliminar esta columna ya que se repite.

- **`Salary`**: Todos los valores son iguales, eliminar esta columna, no aporta valor.

- **`RoleDepartament`**: Eliminar esta columna que es una suma de `JobRole` con `Department` y no aporta valor.

- **`NUMBERCHILDREN`**: Esta columna debe ser eliminada ya que no contiene valores.

- **`StandardHours`**: Variable categórica nominal con un 74% de valores faltantes. Los valores que hay son todos iguales. Eliminar.


### SUGERENCIAS

- Que incluyan la fecha asociada a los registros: Datos recogidos en el 2023 >> Solo para esta columna o para todas? Info en el description de la columna DateBirth.





### NOTAS INICIALES

- Todas las columnas que contienen valores nulos son de tipo `object`.

- `Age`: Variable numérica discreta. Cambiar valores por extenso a numérico y tipo de la columna a `int64`. Crear columna nueva que categorize rangos de edad. 
- `Attrition`: Variable categórica binária. Es un valor histórico, no conocemos el periodo en el que está contabilizado ni el/los tipo/s de rotaciones que contempla (lo consultamos con el PO -Cesar-)
- `BusinessTravel`: Variable categórica nominal con un 48% de valores nulos. Esta variable la utilizaremos en el análisis de forma segmentada, como una muestra del 53% del total de datos. 
Excluiremos todos los registros nulos y hay que mencionar en los análisis que contengan esta variable que estas conclusiones no tienen en cuenta el total de los datos. 
- `DailyRate`: Variable numérica continua. Se debe eliminar el símbolo `$` y convertir el tipo de datos a `float64`. Tiene `nan$` como el valor más frecuente, repitiéndose 124 veces.
Incluye valores numéricos decimales. Pero en el DataFrame aparece como columna de tipo string. Deberás hacer los cambios necesarios para convertirla en columna de tipo numérica.
Analizar la calidad de datos en comparación con las demás variables similares: hourlyRate, monthlyIncome, monthlyRate.
- `Department`: Variable categórica nominal con un 81% de valores nulos. Nos quedamos con esta columna, habría que hacer un strip en los datos. De los 302 datos que hay, 196 son iguales.
Hay que rellenar los datos faltantes de esa columna a partir de la columna 'JobRole' de ser posible. Posibilidad de segmentación por depto. 
- `DistanceFromHome`: Variable numérica discreta. No hay valores faltantes. Tiene 192 valores negativos. Los valores negativos podemos pasarlos a positivos, esto lo hemos verificado con César que nos confirmó que podemos usar los valores absolutos.
- `Education`: Variable categórica ordinal sin valores faltantes, con valores del 1 al 5. 
- `EducationField`: Variable categórica nominal, 6 valores únicos con un 46% de valores nulos. De los datos que hay, 59 son 'Other'. La dejamos como posible análisis Lupa.
- `employeecount`: Variable constante sin valores faltantes, todos los valores son iguales a 1. No aporta valor. Remover esta columna.
- `employeenumber`: Variable categórica nominal, al tratarse de un identificador único para cada empleado (número). Pero estos números están en formato de texto y posiblemente con un formato de decimal que en realidad no es necesario. Hay 534 duplicados en esta columna. Los valores deben ser unicos.  Hablamos con César. debemos analizar los duplicados mejor y tomar decisiones en base a las conclusiones. Por lo que vimos parece que la diferencia entre los duplicados está en Remote Work, puede que sea un error en la carga de datos o que se haya hecho mas de una vez la encuesta. Explorar mas.
- `EnvironmentSatisfaction`: Variable categórica ordinal sin valores faltantes, debería tener valores únicos del 1 al 4, pero un 10% aprox está entre 4 y 1 49, lo que afecta la media. El 90% (1514) son válidos (están entre 1 y 4). Entonces la decisión, en principio, es transformar los vaalores de registros que superan 4 a Nulos y desestimarlos en los cálculos. 
- `Gender`: Variable categórica nominal binária sin valores faltantes. 0 para hombre y 1 para mujer. Hay que reemplazar por "Male" y "Female".
- `HourlyRate`: Variable numérica continua sin valores faltantes, 84 valores = Not Available. Cambiar el tipo de datos a `float` y corregir nos Not Available para que sean Null. 
- `JobInvolvement`: Variable categórica ordinal sin valores faltantes. Cambiar tipo a `object`.
- `JobLevel`: Variable categórica ordinal sin valores faltantes. Cambiar tipo a `object`.
- `JobRole`: Variable categórica nominal sin valores faltantes. Corregir valores: hacer strip y corregir errores tipográficos. Hay un valor '...'
- `JobSatisfaction`: Variable categórica ordinal sin valores faltantes. Tiene valores únicos del 1 al 4. Está OK. Mantener.
- `MaritalStatus`: Variable categórica nominal con un 40% de valores faltantes. Corregir errores tipográficos.
- `MonthlyIncome`: Variable numérica continua con un 52% de valores faltantes. Cambiar tipo a `float64` y comas por puntos.
- `MonthlyRate`: Variable numérica continua sin valores faltantes.
- `NUMCOMPANIESWORKED`: Variable numérica discreta sin valores faltantes, valores de 0-9.
- `Over18`: Variable categórica binária con 56% de valores faltantes. Valores 'Y' y Nan.
- `OverTime`: Variable categórica binária con 42% de valores faltantes. Valores 'No', nan e 'Yes'.
- `PercentSalaryHike`: Variable numérica continua sin valores faltantes.
- `PerformanceRating`: Variable numérica discreta con 12% de valores faltantes. Cambiar tipo a `int64`.
- `RelationshipSatisfaction`: Variable categórica ordinal sin valores faltantes. Tiene valores únicos del 1 al 4. Está OK. Mantener.
- `StandardHours`: Variable categórica nominal con un 74% de valores faltantes. Los valores que hay son todos iguales. >>> ELIMINAR?
- `StockOptionLevel`: Variable categórica ordinal sin valores faltantes. 
- `TOTALWORKINGYEARS`: Variable numérica discreta con un 32% de valores faltantes. Cambiar tipo a `int64`.
- `TrainingTimesLastYear`: Variable numérica discreta sin datos faltantes. 
- `WORKLIFEBALANCE`: Variable categórica ordinal con un 7% de valores faltantes. Cambiar tipo a `int64`.
- `YearsAtCompany`: Variable numérica discreta sin datos faltantes.
- `YearsInCurrentRole`: Variable numérica discreta con un 98% de valores faltantes.
- `YearsSinceLastPromotion`: Variable numérica discreta sin datos faltantes.
- `YEARSWITHCURRMANAGER`: Variable numérica discreta sin datos faltantes.
- `SameAsMonthlyIncome`: Eliminar esta columna ya que se repite.
- `DateBirth`: Variable numérica de intervalo (año de nacimiento) sin valores faltantes.
- `Salary`: Todos los valores son iguales, eliminar esta columna, no aporta valor. 
- `RoleDepartament`: Eliminar esta columna que es una suma de JobRole con Department y no aporta valor. 
- `NUMBERCHILDREN`: Esta columna debe ser eliminada ya que no contiene valores.
- `RemoteWork`: Variable categórica binária sin valores faltantes. Hay que normalizar los valores. 