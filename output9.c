#include <stdio.h>

int main() {
int soma, N, contador;
N = 10;
soma = 0;
contador = 1;
for(int i_1 = 0; i_1 < N; i_1++) {
soma = soma + contador;
contador = contador + 1;
}
printf("%d\n", soma);
return 0;
}