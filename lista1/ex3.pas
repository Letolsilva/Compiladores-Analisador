program TestWhile;

var
  j: integer;

begin
  j := 5;
  while j > 0 do
  begin
    writeln('Valor de j = ', j);
    j := j - 1;
    writeln('AMÉM');
  end;
end.
