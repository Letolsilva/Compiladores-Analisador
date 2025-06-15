program logica;

var
  x, y, z: integer;

begin
  x := 1;
  y := 2;
  z := (x < y) and (y > 0) or not (x = 0);
end.