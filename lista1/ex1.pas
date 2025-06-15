program ExemploCond;

var
  x, y: integer;

begin
  write("Digite um numero: ");
  readln(x);
  if x mod 2 = 0 then
  begin
    y := x * 2;
    writeln('Dobro: ', y);
  end;
  else if x > 10 then
  begin
    y := x + 5;
    writeln('Mais cinco: ', y);
  end;
  else
  begin
    y := x - 3;
    writeln('Menos tres: ', y);
  end;
end.
