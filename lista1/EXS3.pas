program exs3;



var n1,n2: real;

begin;


 writeln ('caro usuario este programa mostrara qual dos numeros que voce inseriu e o maior deles');
 write ('para comecar tecle enter');



 writeln ('por favor digite o primeiro numero e tecle enter ');
 readln (n1);


 writeln ('agora digite o segundo numero e tecle enter ');
 readln (n2);

 //primeiro se le os dois numeros que o usuario digitou, ent�o voce faz as 3 condi��es possiveis, que nesse caso s�o.
 //o n1 maior que o n2, o contrario desta situa��o, e ambos os numeros iguais.
 //ent�o so resta digitar os comandos para cada caso.


 if n1 > n2
   then   begin
          writeln ('o numero maior e , ', n1, '.');
          end;

         else if (n1 < n2)
                then  begin
                      writeln ('o numero maior e , ', n2, '.');
                      end;

                   else if (n1=n2)
                          then begin
                               writeln ('os dois numeros sao iguais.');
                               end;


        writeln (' ');
        write ('para encerrar o programa aperte qualquer tecla.');
       

end.
