program exs2;



var n1,n2,n3,media,exame: real;

begin;


 writeln ('caro usuario agora calcularemos a media de 3 notas e diremos sua situacao.');
 write ('para prosseguir tecle enter');



 writeln ('por favor digite a primeira nota ');
 readln(n1);


 writeln ('por favor digite a segunda nota ');
 readln(n2);


 writeln ('por favor digite a terceira nota ');
 readln(n3);

 //aqui se descobre a media do usuario somando as notas e as dividindo por 3

 //porem a nota do exame, que � a nota que o usuario precisa tirar, se pega a media que ele precisa tirar para passar
 //que no caso � 6 e, subtrai pela media dele das notas que ele tirou.

 media:= (n1+n2+n3)/3;
 exame:= 6-media;



 //aqui coloca o comando para limpar a tela, e se faz a cadeia de ifs, onde so executara a media desejada.

  if (media<=10) and (media >=7)
    then  begin
          writeln ('sua media aritimetica e ', media, ' e voce foi aprovado');
          end;

          else if (media< 7) and (media >=3)
                 then  begin
                       writeln ('sua media aritimetica e ', media, ' voce deve tirar nota ', exame, ' para ser aprovado');
                       end;

                       else if (media <3) and (media >=0)
                              then begin
                                   writeln ('sua media aritimetica e ', media, ' lamento meu caro mas voce foi reprovado estude mais para a proxima.');
                                   end;


 writeln (' ');
 write ('para encerrar o programa precione qualquer tecla ');


end.
