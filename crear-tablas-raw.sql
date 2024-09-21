CREATE TABLE raw_publicaciones (
    id_publicacion INT IDENTITY PRIMARY KEY,
    fecha_publicacion DATE,
    precio_publicacion DECIMAL(10,2),
    tipo_publicacion NVARCHAR(MAX), 
    barrio NVARCHAR(MAX),
    latitud DECIMAL(10,6),
    longitud DECIMAL(10,6),
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE raw_pagos (
    id_pago INT IDENTITY PRIMARY KEY,
    fecha DATE,
    monto DECIMAL(10,2),
    id_publicacion INT, 
    id_usuario INT,
    FOREIGN KEY (id_publicacion) REFERENCES raw_publicaciones(id_publicacion),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE raw_mudanzas (
    id_mudanza INT IDENTITY PRIMARY KEY,
    fecha_solicitud DATE,
    fecha_realizacion DATE,
    costo_mudanza DECIMAL(10,2),
    barrio_origen NVARCHAR(MAX),
    barrio_destino NVARCHAR(MAX),
    latitud_origen DECIMAL(10,6),
    longitud_origen DECIMAL(10,6),
    latitud_destino DECIMAL(10,6),
    longitud_destino DECIMAL(10,6),
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE raw_financiamientos (
    id_financiamiento INT IDENTITY PRIMARY KEY,
    fecha_solicitud DATE,
    monto_solicitado DECIMAL(10,2),
    monto_aprobado DECIMAL(10,2),
    estado_solicitud NVARCHAR(MAX), 
    id_usuario INT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

CREATE TABLE raw_contratos (
    id_contrato INT IDENTITY PRIMARY KEY,
    id_publicacion INT, 
    id_usuario_locador INT,
    id_usuario_locatario INT,
    fecha_firma DATE,
    fecha_inicio DATE,
    fecha_fin DATE,
    monto_renta DECIMAL(10,2),
    estado_contrato NVARCHAR(MAX),
    FOREIGN KEY (id_publicacion) REFERENCES raw_publicaciones(id_publicacion),  
    FOREIGN KEY (id_usuario_locador) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_usuario_locatario) REFERENCES usuarios(id_usuario)
);