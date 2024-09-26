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
    tipo_publicacion NVARCHAR(MAX), 
    barrio NVARCHAR(MAX),
    latitud DECIMAL(10,6),
    longitud DECIMAL(10,6),
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES raw_usuarios(id_usuario) --- El usuario id es 1, 2, 3... y así.
);

CREATE TABLE raw_pagos (
    id_pago INT PRIMARY KEY,
    fecha DATE,
    monto DECIMAL(15,2),
    id_publicacion INT, 
    id_usuario INT,
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

CREATE TABLE raw_contratos (
    id_contrato INT PRIMARY KEY,
    id_publicacion INT, 
    id_usuario_locador INT,
    id_usuario_locatario INT,
    id_usuario_abogado INT, -- Nuevo campo para el abogado
    fecha_firma DATE,
    fecha_inicio DATE,
    fecha_fin DATE,
    monto_renta DECIMAL(15,2),
    estado_contrato NVARCHAR(MAX), -- ['activo, 'finalizado', 'rescindido']
    FOREIGN KEY (id_publicacion) REFERENCES raw_publicaciones(id_publicacion),  
    FOREIGN KEY (id_usuario_locador) REFERENCES raw_usuarios(id_usuario),
    FOREIGN KEY (id_usuario_locatario) REFERENCES raw_usuarios(id_usuario),
    FOREIGN KEY (id_usuario_abogado) REFERENCES raw_usuarios(id_usuario) -- Clave foránea para el abogado
);
