program exs17;



var  a, b, c, delta: real;

begin;

 //depois de se declarar as variaveis se l� os valores de A,B e C que o usuario digitar.


 writeln ('caro usuario este programa resolvera uma equacao de segundo grau e te dara o valor de "x".');
 write ('para comecar precione enter.');



 writeln ('primeiramente digite o valor de "A" sendo que a seja diferente de 0.');
 readln (a);


 writeln ('agora digite o valor de "B"');
 readln (b);


 writeln ('agora digite o valor de "C"');
 readln (c);

 //delta ser� nosso ponto principal pois � dependendo dele que definir� como o programa ir� proceder.
 //caso delta seja menor que 0 ent�o n�o existe raiz real.
 //caso seja 0 h� uma unica raiz real.
 //caso seja maior que 0 h� duas raizes reais.

 delta:= sqr(b) -4*a*c ;



 if (delta < 0) then
    begin
    writeln ('n�o existe raiz real.');
    end

    else if (delta = 0) then
            begin
            writeln ('como delta e 0, a unica raiz real e ', (-b)/(2*a) ,' .');
            end

            else if (delta > 0) then
                    begin
                    writeln ('como delta e maior que 0, as raizes reais sao:');
                    writeln (  (-b + sqrt(delta)) / (2*a), ' e a primeira raiz.');
                    writeln (  (-b - sqrt(delta)) / (2*a), ' e a segunda raiz.');
                    end;

 //ent�o so nos resta mostrar o resultado ao usuario.

 writeln (' ');
 write ('para encerrar o programa precione qualquer tecla.');


end.
