CREATE TABLE Player (
  RFID varchar(255),
  name varchar(255),
  wins int,
  defeats int,
  PRIMARY KEY(RFID),
  CHECK (wins >= 0),
  CHECK (defeats >= 0)
);

