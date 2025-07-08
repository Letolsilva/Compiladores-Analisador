program exOpHexa;
var
  a, b, c: integer;
  nome: string;
begin
  a := 0xFF + 0755;        
  b := 0755;         
  c := a + b;       
  c := 0xFF + 10;   
  c := 0755 + 100; 
  writeln(a);
  writeln(b);
  writeln(c);
end.