program exemplo;

var
  x, y: integer;
  resultado1: real;
  resultado2: integer;

begin
  x := 10;
  y := 3;

  writeln('=== TESTE DE DIVISÕES ===');
  writeln('x = ', x);
  writeln('y = ', y);

  resultado1 := x / y;
  writeln('x / y = ', resultado1);

  resultado2 := x div y;
  writeln('x div y = ', resultado2);

  resultado2 := x mod y;
  writeln('x mod y = ', resultado2);

end.