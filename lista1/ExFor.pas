program teste_for_aninhado;

var
  i, j: integer;

begin
  for i := 1 to 3 do
  begin
    for j := 1 to 2 do
    begin
      writeln('i=', i, ' j=', j);
    end;
  end;
end.