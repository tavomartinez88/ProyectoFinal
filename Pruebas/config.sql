drop schema if exists DjangoTest;
CREATE schema DjangoTest;

DROP TABLE IF EXISTS  DjangoTest.jugadores ;
CREATE TABLE  DjangoTest.jugadores  (
   DNI  int NOT NULL,
   NOMBRE  varchar(40) NOT NULL,
   APELLIDO  varchar(40) NOT NULL,
   EMAIL varchar(40) NOT NULL,
   TEL1 int,
   TEL2 int,
   DIRECCION varchar(60),
   USERNAME varchar(40) NOT NULL UNIQUE,
   PASSWORD varchar(40) NOT NULL,
  PRIMARY KEY  ( USERNAME )
);