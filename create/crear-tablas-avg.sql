----------------------- ALQUILERES

CREATE TABLE avg_resumen_alquileres (
    barrio NVARCHAR(255) PRIMARY KEY,
    total_alquileres INT,
    renta_promedio DECIMAL(15,2),
    ingreso_total DECIMAL(15,2),
    renta_maxima DECIMAL(15,2),
    renta_minima DECIMAL(15,2)
);


------------------------ MUDANZAS

CREATE TABLE avg_costo_mudanza_por_barrio (
    barrio NVARCHAR(255) PRIMARY KEY,
    costo_promedio_mudanza DECIMAL(10,2),
    mudanzas_realizadas INT
);

CREATE TABLE avg_distancia_mudanza_por_mes (
    anio INT,
    mes INT,
    distancia_promedio DECIMAL(15, 2),
    mudanzas_realizadas INT,
    PRIMARY KEY (anio, mes)
);

CREATE TABLE avg_mudanzas_por_barrio_destino (
    barrio_destino NVARCHAR(255) PRIMARY KEY,
    total_mudanzas INT
);

CREATE TABLE avg_mudanzas_por_barrio_origen (
    barrio_origen NVARCHAR(255) PRIMARY KEY,
    total_mudanzas INT
);

CREATE TABLE avg_mudanzas_por_barrio_combinacion (
    barrio_origen NVARCHAR(255),
    barrio_destino NVARCHAR(255),
    total_mudanzas INT,
    PRIMARY KEY (barrio_origen, barrio_destino)
);

-------------------------------------

CREATE TABLE avg_actividad_usuarios (
    fecha DATE,
    tipo_usuario NVARCHAR(MAX),
    nuevos_usuarios INT,
    usuarios_activos INT,
    tasa_retencion DECIMAL(10,4)
);

CREATE TABLE avg_detalles_pagos (
    fecha DATE,
    monto_total_recibido DECIMAL(10,2),
    pagos_vencidos INT,
    promedio_pago_vencido DECIMAL(10,2),
    promedio_pago_recibido DECIMAL(10,2)
);

CREATE TABLE avg_tasaciones_por_barrio (
    fecha DATE,
    barrio NVARCHAR(MAX),
    valor_tasacion_promedio DECIMAL(10,2),
    tasacion_maxima DECIMAL(10,2),
    tasacion_minima DECIMAL(10,2),
    cantidad_tasaciones INT
);

CREATE TABLE avg_costo_mudanza (
    fecha DATE,
    costo_promedio_mudanza DECIMAL(10,2),
    costo_maximo_mudanza DECIMAL(10,2),
    costo_minimo_mudanza DECIMAL(10,2)
);




CREATE TABLE avg_financiamientos (
    fecha DATE,
    monto_total_financiado DECIMAL(10,2),
    solicitudes_aprobadas INT,
    tasa_aprobacion DECIMAL(10,4)
);