CREATE TABLE Player (
  ID int8 NOT NULL,
  RFID varchar(255),
  name varchar(255),
  wins int8,
  defeats int8,
  PRIMARY KEY(ID),
  CHECK (wins >= 0),
  CHECK (defeats >= 0)
);

