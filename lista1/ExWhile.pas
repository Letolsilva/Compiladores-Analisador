program teste_while_aninhado;

var
  i, j: integer;

begin
  i := 1;
  while i <= 3 do
  begin
    j := 1;
    while j <= 2 do
    begin
      writeln('i=', i, ' j=', j);
      j := j + 1;
    end;
    i := i + 1;
  end;
end.