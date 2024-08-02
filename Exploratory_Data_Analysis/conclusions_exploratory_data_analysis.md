# CONCLUSIONES

## Columnas y su tipo de variable

### Variables Numéricas

- **`Age`**
   - Tipo: Variable numérica discreta.
   - Limpieza y transformación: ✅
        - Convertir valores textuales a numéricos.
        - Cambiar el tipo de la columna a `int64`.
        - Crear una columna nueva que categorice rangos de edad para análisis segmentado.

- **`DailyRate`**
    - Tipo: Variable numérica continua.
    - Limpieza y transformación: ✅
        - Eliminar el símbolo `$` y convertir el tipo de datos a `float64`.
        - Revisar y corregir el valor frecuente `nan$` (repite 124 veces).
        - Analizar la calidad de datos en comparación con otras variables relacionadas: `HourlyRate`, `MonthlyIncome`, `MonthlyRate`.
    - Nulos: 7% - Imputación a definir (hay que convertir antes a tipo numérico para ver si tiene outliers, verificar media/mediana) 
    
- **`DistanceFromHome`**
    - Tipo: Variable numérica discreta.
    - Limpieza y transformación: ✅
        - Convertir 192 valores negativos a positivos, según confirmación de César.
        - Hay que verificar si los negativos están en el mismo rango de los positivos para justificar esta decisión. 

- **`HourlyRate`**
    - Tipo: Variable numérica continua.
    - Limpieza y transformación: ✅
        - Cambiar el tipo de datos a `float`.
    - Nulos: 5% - Corregir 84 valores "Not Available". Imputación a definir. (hay que convertir antes a tipo numérico para ver si tiene outliers, verificar media/mediana) 

- **`MonthlyIncome`**
    - Tipo: Variable numérica continua.
    - Limpieza y transformación: ✅
        - Cambiar el tipo de datos a `float64`.
        - Sustituir comas por puntos.
    - Nulos: 52% - Ya que tiene un alto número de nulos, podemos prescindir de esa columna si encontramos estos mismos datos en otro columna? Hay que buscar a ver si podemos sustituir estos datos usando otra columa, y si no, ver si tiene sentido imputar estos nulos con los datos de otra columna que esté relacionada.
    Imputación a definir (hay que convertir antes a tipo numérico para ver si tiene outliers, verificar media/mediana)
     
- **`MonthlyRate`**
    - Tipo: Variable numérica continua

- **`NUMCOMPANIESWORKED`**
    - Tipo: Variable numérica discreta
      - Contiene valores de 0-9.

- **`PercentSalaryHike`**
    - Tipo: Variable numérica continua

- **`PerformanceRating`**
    - Tipo: Variable numérica discreta.
    - Limpieza y transformación: ✅
        - Cambiar el tipo de datos a `int64`.
    - Nulos: 12% - Imputar por la moda?
    Esto puede sesgar los datos hacia el valor dominante, reduciendo la variabilidad y potencialmente ocultando patrones en los datos.
    Imputación Condicional: Imputar los valores nulos basándose en subgrupos o categorías. Por ejemplo, si hay otros datos disponibles que correlacionen fuertemente con PerformanceRating, se puede usar esta información para una imputación más precisa.
    No Imputar: En algunos casos, puede ser mejor dejar los valores nulos y usar técnicas que manejen los nulos explícitamente durante el análisis.

- **`TOTALWORKINGYEARS`**
    - Tipo: Variable numérica discreta.
    - Limpieza y transformación: ✅
        - Cambiar las comas por puntos.
        - Cambiar el tipo de datos a `int64`.
        - Hay un valor 0.0 que se repite 8 veces, será un empleado que tiene menos de 1 año de experiencia?
    - Nulos: 32% - - Imputar por la mediana? También se puede considerar una columna nueva en el caso que valor nulo signifique empleados nuevos.
    Verificar relación de esta columna con las demás antes de decidir si estos nulos los imputamos o no. 

- **`TrainingTimesLastYear`**
    - Tipo: Variable numérica discreta.

- **`YearsAtCompany`**
    - Tipo: Variable numérica discreta.

- **`YearsSinceLastPromotion`**
    - Tipo: Variable numérica discreta.

- **`YEARSWITHCURRMANAGER`**
    - Tipo: Variable numérica discreta.

- **`DateBirth`**
    - Tipo: Variable numérica de intervalo (año de nacimiento).


### Variables Categóricas

- **`Attrition`**
    - Tipo: Variable categórica binaria.
     - Revisar contexto y periodo de tiempo representado con el equipo de producto.

- **`BusinessTravel`**
    - Tipo: Variable categórica nominal.
    - Nulos: 48% - Utilizar en el análisis de forma segmentada, excluyendo registros nulos.
    Verificar relación de esta columna con las demás antes de tomar decisiones.
    Reemplazar valores nulos por distribución aunque la moda sea sifnificativac (Travel_Rarely). El % de nulos es demasiado. >> Unknown

- **`Department`**
    - Tipo: Variable categórica nominal.
    - Limpieza y transformación: ✅
        - Rellenar datos faltantes a partir de la columna `JobRole` si es posible.
        - Realizar `strip` en los datos existentes.
    Nulos: 81% - Intentaremos imputar con los datos de `JobRole` y/o `RoleDepartament`.
    se imputa por la moda

- **`Education`**
    - Tipo: Variable categórica ordinal.
     - Valores del 1 al 5.

- **`EducationField`**
    - Tipo: Variable categórica nominal.
     - Contiene 6 valores únicos.
    - Nulos: 46% - Verificar relación de esta columna con las demás antes de tomar decisiones.
    Imputar por moda (life sciences) --> la más sencilla si creemos que la info que nos puede aportar no es muy significativa.
    Imputar por distribución --> refleja mejor la distribución real.
    En un princio había pensado en correlacionarla con JobRole, pero creo que no es necesario para lo que podemos sacar. 

- **`employeenumber`**
    - Tipo: Variable categórica nominal.
    - Limpieza y transformación: ✅
        - Transformar el tipo de dato a entero, eliminando formato decimal innecesario.
    - Duplicados: Identificador único para cada empleado, pero contiene 534 duplicados. 
    Decidimos quedarnos con los IDs de índice mas alto por considerar que puede ser el mas actualizado. 
    - Nulos: 26,7% - Buscar algún patrón en estos nulos y si no hay, asignarles IDs únicos a partir del último que tenemos o dejar estos empleados sin ID. Otra opción seria resetear los IDS y asignar nuevos IDs consecutivos a todos los empleados. 
    Analizar si los registros con nulos en empleado_ID contienen información valiosa en otras columnas.
    IMPORTANTE: Puede que un empleado con id nulo sea el mismo empleado que tenga un ID?? Habría que verificar esto. 

- **`EnvironmentSatisfaction`**
    - Tipo: Variable categórica ordinal.
    - Limpieza y transformación: ✅
        - Transformar valores mayores a 4 a nulos y excluirlos de los cálculos.
    Nulos: 6% - Verificar relación de esta columna con las demás antes de tomar decisiones de cómo imputar estos nulos.

- **`Gender`**
    - Tipo: Variable categórica nominal binaria.
    - Limpieza y transformación: ✅
        - Reemplazar valores por "Male" y "Female".
        - Cómo elegir male o female? Mirar los sueldos mas altos, serán male. 

- **`JobInvolvement`**
    - Tipo: Variable categórica ordinal.

- **`JobLevel`**
    - Tipo: Variable categórica ordinal.

- **`JobRole`**
    - Tipo: Variable categórica nominal.
    - Limpieza y transformación: ✅
        - Corregir valores con `strip` y errores tipográficos.

- **`JobSatisfaction`**
    - Tipo: Variable categórica ordinal.
      - Valores del 1 al 4.

- **`MaritalStatus`**
    - Tipo: Variable categórica nominal.
    - Limpieza y transformación: ✅
        - Corregir errores tipográficos.
    - Nulos: 40% - Verificar relación de esta columna con las demás antes de tomar decisiones.

- **`OverTime`**
    - Tipo: Variable categórica binaria.
    - Limpieza y transformación: ✅
        - Valores: "No", `NaN`, y "Yes".
    - Nulos: 42% - Verificar relación de esta columna con las demás antes de tomar decisiones.

- **`RelationshipSatisfaction`**
    - Tipo: Variable categórica ordinal.
      - Valores del 1 al 4.

- **`StockOptionLevel`**
    - Tipo: Variable categórica ordinal.
      - Valores del 0 al 3.

- **`WORKLIFEBALANCE`**
    - Tipo: Variable categórica ordinal.
      - Valores del 1 al 4.
    - Limpieza y transformación: ✅
      - Cambiar tipo de datos a `int64`.
    - Nulos: 7% - Imputar por moda dado el bajo % de nulos.

- **`RemoteWork`**
    - Tipo: Variable categórica binaria.
    - Limpieza y transformación: ✅
      - Normalizar los valores.


### Variables a Eliminar

- **`employeecount`**
    - Motivo: Variable constante sin valores faltantes, todos los valores son iguales a 1. No aporta valor. Remover esta columna.

- **`SameAsMonthlyIncome`**
    - Motivo: Eliminar esta columna ya que se repite.

- **`Salary`**
    - Motivo: Todos los valores son iguales, eliminar esta columna, no aporta valor.

- **`RoleDepartament`**
    - Motivo: Eliminar esta columna que es una suma de `JobRole` con `Department`, tras haberla usado para recuperar la columna `Department`.

- **`NUMBERCHILDREN`**
    - Motivo: Esta columna debe ser eliminada ya que no contiene valores.

- **`StandardHours`**
    - Motivo: Variable categórica nominal con un 74% de valores faltantes. Los valores que hay son todos iguales. Eliminar.

- **`Yearsincurrentrole`**
    - Motivo: Esta columna debe ser eliminada ya que tiene un 98% valores faltantes.

- **`Over18`**
    - Motivo: Esta columna no es necesaria ya que podemos saber si el empleado es mayor de 18 a partir de la columna `Age`.


### NULOS

# DailyRate                7.00 > media
# HourlyRate               5.00 > media
# MonthlyIncome           52.23 > Agrupar por JobRole e imputar por KNN o interative imputer
# PerformanceRating       12.08 > mediana
# TOTALWORKINGYEARS       32.59 > KNN o interative imputer
# employeenumber          26.70 > KNN o interative imputer
# EnvironmentSatisfaction  6.00 > mediana
# WORKLIFEBALANCE          6.69 > mediana

# BusinessTravel          47.83 > unknown
# Department              81.29 > distribución de frecuencia
# EducationField          46.16 > unknown
# MaritalStatus           40.33 > unknown
# OverTime                41.88 > unknown



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
