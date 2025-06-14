program exemplo;

var
  x, y: integer;
  nome: string;

begin
  x := 10;
  y := 20;
  nome := 'grupo4';

  if (x < y) or (2 < 3) and not (x = 10) and (5 > 9) then
    writeln('Condicao verdadeira');

end.