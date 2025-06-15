program TestForCorrigido;

var
  i, k: integer;

begin
  k := 0;

  for i := 1 to 5 do
  begin
    writeln('Valor de i = ', i);
    k := k + 2;    { agora faz parte do loop }
  end;
  writeln('\nValor de k = ', k);
end.
