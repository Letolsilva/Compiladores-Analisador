program exs21;



var cod_e,cod_c: integer;
var peso,novo_peso: real;

begin;

 //depois de se declarar as variaveis se apresenta o programa ao usuario.


 writeln ('caro usuario este programa programa lhe mostrara de acordo com os dados que voce inserir, o peso da carga do caminhao.');
 writeln ('o preco da carga do caminhao, o valor do imposto do estado, e o valor do produto acrescido do imposto.');
 writeln (' ');
 write ('para inciar tecle enter.');


 //voc� ler� do usuario dois codigos que ser�o utilizados na estrutura case e um valor que � o peso da carga em toneladas.


 writeln ('primeiramente digite o codigo do estado de origem, de 1 a 5.');
 readln (cod_e);


 writeln ('agora digite o codigo da carga, de 10 a 40.');
 readln (cod_c);


 writeln ('agora digite o peso da carga em toneladas.');
 readln (peso);

 novo_peso:= peso*1000;

 //se transforma o peso em toneladas em quilos e se come�a as estruturas case.



 {a estrutura primaria � a que tem como condi��o o codigo de estado que definira o imposto.
 a estrutura secundaria que entra dentro de todas as primarias � a que tem como condi��o o codigo do produto que definir� o seu pre�o.
 ent�o se faz os calculos para cada estrutura considerando o valor de imposto, e o pre�o de cada quilo de produto.
 e se apresenta ao usuario esses resultados.}

 case cod_e of

   1: case cod_c of
      10..20: begin
              writeln ('o peso da carga em quilos e ', novo_peso, ' .');
              writeln ('o preco da carga e ', (novo_peso * 100), ' .');
              writeln ('o preco do imposto e ', ((novo_peso * 100) *0.35), ' .');
              writeln ('o valor da carga com imposto e ', ((novo_peso * 100) *1.35), ' .');
              end;

      21..30: begin
              writeln ('o peso da carga em quilos e ', novo_peso, ' .');
              writeln ('o preco da carga e ', (novo_peso * 250), ' .');
              writeln ('o preco do imposto e ', ((novo_peso * 250) *0.35), ' .');
              writeln ('o valor da carga com imposto e ', ((novo_peso * 250) *1.35), ' .');
              end;

      31..40: begin
              writeln ('o peso da carga em quilos e ', novo_peso, ' .');
              writeln ('o preco da carga e ', (novo_peso * 340), ' .');
              writeln ('o preco do imposto e ', ((novo_peso * 340) *0.35), ' .');
              writeln ('o valor da carga com imposto e ', ((novo_peso * 340) *1.35), ' .');
              end;
      end;

   2: case cod_c of
      10..20: begin
              writeln ('o peso da carga em quilos e ', novo_peso, ' .');
              writeln ('o preco da carga e ', (novo_peso * 100), ' .');
              writeln ('o preco do imposto e ', ((novo_peso * 100) *0.25), ' .');
              writeln ('o valor da carga com imposto e ', ((novo_peso * 100) *1.25), ' .');
              end;

      21..30: begin
              writeln ('o peso da carga em quilos e ', novo_peso, ' .');
              writeln ('o preco da carga e ', (novo_peso * 250), ' .');
              writeln ('o preco do imposto e ', ((novo_peso * 250) *0.25), ' .');
              writeln ('o valor da carga com imposto e ', ((novo_peso * 250) *1.25), ' .');
              end;

      31..40: begin
              writeln ('o peso da carga em quilos e ', novo_peso, ' .');
              writeln ('o preco da carga e ', (novo_peso * 340), ' .');
              writeln ('o preco do imposto e ', ((novo_peso * 340) *0.25), ' .');
              writeln ('o valor da carga com imposto e ', ((novo_peso * 340) *1.25), ' .');
              end;
      end;


   3: case cod_c of
      10..20: begin
              writeln ('o peso da carga em quilos e ', novo_peso, ' .');
              writeln ('o preco da carga e ', (novo_peso * 100), ' .');
              writeln ('o preco do imposto e ', ((novo_peso * 100) *0.15), ' .');
              writeln ('o valor da carga com imposto e ', ((novo_peso * 100) *1.15), ' .');
              end;

      21..30: begin
              writeln ('o peso da carga em quilos e ', novo_peso, ' .');
              writeln ('o preco da carga e ', (novo_peso * 250), ' .');
              writeln ('o preco do imposto e ', ((novo_peso * 250) *0.15), ' .');
              writeln ('o valor da carga com imposto e ', ((novo_peso * 250) *1.15), ' .');
              end;

      31..40: begin
              writeln ('o peso da carga em quilos e ', novo_peso, ' .');
              writeln ('o preco da carga e ', (novo_peso * 340), ' .');
              writeln ('o preco do imposto e ', ((novo_peso * 340) *0.15), ' .');
              writeln ('o valor da carga com imposto e ', ((novo_peso * 340) *1.15), ' .');
              end;
      end;

   4: case cod_c of
      10..20: begin
              writeln ('o peso da carga em quilos e ', novo_peso, ' .');
              writeln ('o preco da carga e ', (novo_peso * 100), ' .');
              writeln ('o preco do imposto e ', ((novo_peso * 100) *0.05), ' .');
              writeln ('o valor da carga com imposto e ', ((novo_peso * 100) *1.05), ' .');
              end;

      21..30: begin
              writeln ('o peso da carga em quilos e ', novo_peso, ' .');
              writeln ('o preco da carga e ', (novo_peso * 250), ' .');
              writeln ('o preco do imposto e ', ((novo_peso * 250) *0.05), ' .');
              writeln ('o valor da carga com imposto e ', ((novo_peso * 250) *1.05), ' .');
              end;

      31..40: begin
              writeln ('o peso da carga em quilos e ', novo_peso, ' .');
              writeln ('o preco da carga e ', (novo_peso * 340), ' .');
              writeln ('o preco do imposto e ', ((novo_peso * 340) *0.05), ' .');
              writeln ('o valor da carga com imposto e ', ((novo_peso * 340) *1.05), ' .');
              end;
      end;

   5: case cod_c of
      10..20: begin
              writeln ('o peso da carga em quilos e ', novo_peso, ' .');
              writeln ('o preco da carga e ', (novo_peso * 100), ' .');
              writeln ('o preco do imposto e ', ((novo_peso * 100) *0.0), ' .');
              writeln ('o valor da carga com imposto e ', ((novo_peso * 100) *1.00), ' .');
              end;

      21..30: begin
              writeln ('o peso da carga em quilos e ', novo_peso, ' .');
              writeln ('o preco da carga e ', (novo_peso * 250), ' .');
              writeln ('o preco do imposto e ', ((novo_peso * 250) *0.00), ' .');
              writeln ('o valor da carga com imposto e ', ((novo_peso * 250) *1.00), ' .');
              end;

      31..40: begin
              writeln ('o peso da carga em quilos e ', novo_peso, ' .');
              writeln ('o preco da carga e ', (novo_peso * 340), ' .');
              writeln ('o preco do imposto e ', ((novo_peso * 340) *0.00), ' .');
              writeln ('o valor da carga com imposto e ', ((novo_peso * 340) *1.00), ' .');
              end;
      end;

 end;

 writeln (' ');
 write ('para encerrar o programa precione qualquer tecla.');


end.
