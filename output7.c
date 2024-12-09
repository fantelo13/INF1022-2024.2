#include <stdio.h>

int main() {
int resultado;
resultado = 1;
for(int i_1 = 0; i_1 < 3; i_1++) {
resultado = resultado * 2;
}
printf("%d\n", resultado);
return 0;
}