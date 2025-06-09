program exemplo;

var
  x, y: integer;
  nome: string;

begin
  x := 10;
  y := 20;
  nome := 'grupo4';

  if x < y then
    if y > 15 then
      writeln(nome);
    else
      writeln('Y menor ou igual a 15');
  else
    writeln('Outro nome');
end.