program exs16;



var n1: integer;
    n2: real;

begin;

 //depois de se declarar as variaveis, se apresenta um resumo do programa ao usuario.


 writeln ('caro usuario este programa lhe mostrara o novo preco do produto de acordo com a venda mensal e seu pre�o.');
 write ('para prosseguir tecle enter.');


 //se le os valores do pre�o do produto e da venda mensal do mesmo.


 writeln ('por favor digite o preco do produto.');
 readln (n1);


 writeln ('agora digite a venda mensal do produto');
 readln (n2);



 //e depois se come�a a cadeia de ifs para determinar o novo pre�o do produto
 //com as condi��es impostas j� se apresenta ao usuario o novo valor do produto fazendo simples calculos de mutiplica��o.

 if (n2 >= 1200) or  (n1 >= 80) then
    begin
    writeln ('o novo preco do produto e ', n1*0.80, ' .');
    end

    else if (n2 >= 500) or ((n1 >= 30) and (n1<80)) then
            begin
            writeln ('o novo preco do produto e ', n1*0.15, ' .');
            end

            else if (n2<500) or (n1<30) then
                    begin
                    writeln ('o novo preco do produto e ', n1*0.10, ' .');
                    end;

 writeln (' ');
 write ('para encerrar o programa precione qualquer tecla.');


end.
