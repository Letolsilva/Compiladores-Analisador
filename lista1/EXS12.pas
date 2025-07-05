program exs12;



var n1: integer;
    sal: real;

begin;

 //se apresenta o resumo do programa para o usuario.


 writeln ('caro usuario este programa lhe apresentara seu novo salario de acordo com seu cargo.');
 write ('para comecar tecle enter.');


 //Ent�o se le o salario que o usuario ira digitar.


 writeln ('primeiramente digite o seu salario.');
 readln (sal);

 //depois se le a op��o que definir� quanto de salario o usuario ir� receber.


 writeln ('para calcular seu novo salario , ');
 writeln (' ');
 writeln ('tecle 1 caso voce seja escriturario.');
 writeln ('tecle 2 caso voce seja secretario.');
 writeln ('tecle 3 caso voce seja caixa.');
 writeln ('tecle 4 caso voce seja gerente.');
 writeln ('tecle 5 caso voce seja diretor.');
 readln (n1);



 //E com uma simples estrutura de case engloba as op��es e da o tratamento para cada uma delas.
 //Entao de acordo com a op��o que o usuario digitar se apresenta direto o novo salario dele ja com o aumento.

 case n1 of

   1:  writeln ('seu novo salario e de ', sal*1.5, ' .');
   2:  writeln ('seu novo salario e de ', sal*1.35, ' .');
   3:  writeln ('seu novo salario e de ', sal*1.2, ' .');
   4:  writeln ('seu novo salario e de ', sal*1.1, ' .');
   5:  writeln ('seu novo salario e de ', sal , ' .');

 end;

 writeln (' ');
 write ('para encerrar o programa precione qualquer tecla.');  

end.