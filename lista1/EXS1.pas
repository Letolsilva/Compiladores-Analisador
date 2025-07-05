program exs1;

var n1,n2,n3,n4: real;

begin;


 writeln ('caro usuario este programa calculara 3 notas com seus respesquitivos pesos e a media da nota sera o conceito recebido.');
 write ('para comecar aperte enter ');



 writeln ('primeiro declare a nota do trabalho de laboratorio com peso 2 ');
 readln(n1);


 writeln ('agora declare a nota da avaliacao semestral com peso 3 ');
 readln(n2);


 writeln ('por fim declare a nota do exame final com peso 5 ');
 readln(n3);

 //foi pego as notas que o usuario declarou e a media feita pela soma de cada um com seus pesos dividido pelo
 //numero dos pesos somados
 n4:= ((n1*2)+(n2*3)+(n3*5))/10;


  //aqui foi colocado varias condicionais uma dentro da outra para que quando a media for encontrada o programa parar
  //de executar e ja mostrar a mensagem direto pro usuario de seu conceito.
 if ((n4<=10) and (n4>=8))
 then  begin
       writeln ('caro usuario sua media e ', n4, ' e seu conceito e A');
       end;

      else  if  ((n4<8) and (n4>=7))
            then  begin
                  writeln ('caro usuario sua media e ', n4, ' e seu conceito e B');
                  end;

                  else if (n4<7) and (n4>=6)
                        then  begin
                              writeln ('caro usuario sua media e ', n4, ' e seu conceito e C');
                              end;

                              else if (n4<6) and (n4>=5)
                                    then  begin
                                          writeln ('caro usuario sua media e ' , n4, ' e seu conceito e D');
                                          end;

                                          else if (n4<5) and (n4>=0)
                                                then  begin
                                                      writeln ('caro usuario sua media e ', n4, ' e seu conceito e E');
                                                      end;

 writeln (' ');
 write ('para encerrar o programa aperte qualquer tecla.');


end.
