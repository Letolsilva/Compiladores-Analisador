program ExemploReadCorrigido;

var
  nome: string;
  idade: integer;
  altura: real;

begin
  write('Digite seu nome: ');
  readln(nome);    

  write('Digite sua idade: ');
  readln(idade);

  write('Digite sua altura em metros (ex: 1.75): ');
  readln(altura);

  writeln('--- Resultado ---');
  writeln('Nome: ', nome);
  writeln('Idade: ', idade);
  writeln('Altura: ', altura, ' m');
end.