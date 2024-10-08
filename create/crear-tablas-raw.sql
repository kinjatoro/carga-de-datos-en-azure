CREATE TABLE raw_usuarios (
    id_usuario INT PRIMARY KEY,
    nombre NVARCHAR(MAX),
    tipo_usuario NVARCHAR(MAX), -- Puede ser 'locador', 'locatario', 'empleado', 'mudanza', 'abogado'
    fecha_registro DATE,
);

CREATE TABLE raw_publicaciones (
    id_publicacion INT PRIMARY KEY,
    fecha_publicacion DATE,
    precio_publicacion DECIMAL(15,2),
    direccion NVARCHAR(MAX),
    habitaciones INT,
    barrio NVARCHAR(MAX),
    latitud DECIMAL(10,6),
    longitud DECIMAL(10,6),
    estado NVARCHAR(10), --- Activo o inactivo
    id_usuario INT,
    tipo NVARCHAR(15), --- Casa o departamento
    superficie_total_m2 INT, --- En metros cuadrados,
    ganancia_generada DECIMAL(15,2),
    FOREIGN KEY (id_usuario) REFERENCES raw_usuarios(id_usuario) --- El usuario id es 1, 2, 3... y así.
);

CREATE TABLE raw_pagos (
    id_pago INT PRIMARY KEY,
    fecha DATE,
    monto DECIMAL(15,2),
    id_publicacion INT, 
    id_usuario INT,
    estado NVARCHAR(MAX), --- 'Aprobado, pendiente, rechazado'
    FOREIGN KEY (id_publicacion) REFERENCES raw_publicaciones(id_publicacion),
    FOREIGN KEY (id_usuario) REFERENCES raw_usuarios(id_usuario)
);

CREATE TABLE raw_mudanzas (
    id_mudanza INT PRIMARY KEY,
    fecha_solicitud DATE,
    fecha_realizacion DATE,
    costo_mudanza DECIMAL(15,2),
    barrio_origen NVARCHAR(MAX),
    barrio_destino NVARCHAR(MAX),
    latitud_origen DECIMAL(10,6),
    longitud_origen DECIMAL(10,6),
    latitud_destino DECIMAL(10,6),
    longitud_destino DECIMAL(10,6),
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES raw_usuarios(id_usuario)
);

CREATE TABLE raw_financiamientos (
    id_financiamiento INT PRIMARY KEY,
    fecha_solicitud DATE,
    monto_solicitado DECIMAL(15,2),
    monto_aprobado DECIMAL(15,2),
    estado_solicitud NVARCHAR(MAX), ---- ['aprobado', 'pendiente', 'rechazado']
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES raw_usuarios(id_usuario)
);


/*
Asignado: cuando solo firmó una de las partes (locador o locatario), o ninguna de ellas.
Pendiente: cuando ya firmaron ambas partes, pero aún falta la firma del escribano.
Activo: cuando locador, locatario y escribano han firmado.
Finalizado: cuando el contrato ya ha terminado por fecha.
Rescindido: cuando el contrato se termina antes de su fecha de finalización.
Rechazado: cuando alguna de las partes o el escribano rechazan el contrato antes de la firma final.
*/

CREATE TABLE raw_contratos (
    id_contrato INT PRIMARY KEY,
    id_publicacion INT, 
    id_usuario_locatario INT,
    id_usuario_locador_o_mudanza INT,
    id_usuario_escribano INT, -- Nuevo campo para el escribano (firma digital)
    tipo_contrato NVARCHAR(50), -- ['Alquiler', 'Guardado muebles', 'Mudanza']
    fecha_firma DATE,
    fecha_inicio DATE,
    fecha_fin DATE,
    monto DECIMAL(15,2), -- Puede ser alquiler o monto del guardado de muebles
    estado_contrato NVARCHAR(MAX), -- ['activo', 'finalizado', 'rescindido', 'rechazado', 'pendiente', 'asignado']
    FOREIGN KEY (id_publicacion) REFERENCES raw_publicaciones(id_publicacion),  
    FOREIGN KEY (id_usuario_locador_o_mudanza) REFERENCES raw_usuarios(id_usuario),
    FOREIGN KEY (id_usuario_locatario) REFERENCES raw_usuarios(id_usuario),
    FOREIGN KEY (id_usuario_escribano) REFERENCES raw_usuarios(id_usuario), -- Clave foránea para el escribano
);


CREATE TABLE raw_reclamos (
    id_reclamo INT PRIMARY KEY,
	fecha_reclamo DATE,
    estado NVARCHAR(50), --  ("Abierto", "En Proceso", "Resuelto", "Cerrado")
	id_usuario INT,
	categoria NVARCHAR(50), --  (Categoría específica como "Problemas Técnicos", "Cobros Incorrectos", "Servicio Deficiente", “Otros”, etc.)
    FOREIGN KEY (id_usuario) REFERENCES raw_usuarios(id_usuario),  
);
