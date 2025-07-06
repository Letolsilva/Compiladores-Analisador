program ExemploBreakContinue;

var
  i, idade: integer;

begin
  for i := 1 to 5 do
  begin
    write('Digite sua idade (digite 0 para sair): ');
    readln(idade);

    if idade = 0 then
    begin
      writeln('Saindo do loop com break.');
      break;
    end;

    if idade < 0 then
    begin
      writeln('Idade inválida, tente novamente (continue).');
      continue;
    end;

    writeln('Idade informada: ', idade);
  end;

  writeln('Fim do programa.');
end.