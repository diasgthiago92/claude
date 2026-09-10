#!/usr/bin/env python3
"""
Validação de CNPJ - Exemplo Básico
"""

def validar_cnpj(cnpj):
    """
    Valida se um CNPJ é válido (módulo 11).
    """
    # Remove caracteres especiais
    cnpj = str(cnpj).replace(".", "").replace("/", "").replace("-", "")

    # Deve ter 14 dígitos
    if len(cnpj) != 14 or not cnpj.isdigit():
        return False

    # CNPJ nulo (todos iguais) é inválido
    if cnpj == cnpj[0] * 14:
        return False

    # Calcula primeiro dígito verificador
    tamanho = len(cnpj) - 2
    numeros = cnpj[:tamanho]
    digitos = cnpj[tamanho:]
    soma = 0
    pos = tamanho - 1

    for i in range(tamanho):
        soma += int(numeros[i]) * (pos - i)

    resultado = soma % 11
    dv1 = 0 if resultado < 2 else 11 - resultado

    if int(digitos[0]) != dv1:
        return False

    # Calcula segundo dígito verificador
    numeros = cnpj[:tamanho + 1]
    soma = 0
    pos = tamanho

    for i in range(tamanho + 1):
        soma += int(numeros[i]) * (pos - i)

    resultado = soma % 11
    dv2 = 0 if resultado < 2 else 11 - resultado

    if int(digitos[1]) != dv2:
        return False

    return True


def formatar_cnpj(cnpj):
    """
    Formata CNPJ para: XX.XXX.XXX/XXXX-XX
    """
    cnpj = str(cnpj).replace(".", "").replace("/", "").replace("-", "")

    if len(cnpj) != 14:
        return None

    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"


# Exemplos de uso
if __name__ == "__main__":
    # CNPJ válido
    cnpj_valido = "11222333000181"
    print(f"CNPJ: {cnpj_valido}")
    print(f"Válido: {validar_cnpj(cnpj_valido)}")
    print(f"Formatado: {formatar_cnpj(cnpj_valido)}")
    print()

    # CNPJ inválido
    cnpj_invalido = "11111111111111"
    print(f"CNPJ: {cnpj_invalido}")
    print(f"Válido: {validar_cnpj(cnpj_invalido)}")
    print()

    # Amazon (CNPJ real)
    cnpj_amazon = "15436940000172"
    print(f"CNPJ: {cnpj_amazon}")
    print(f"Válido: {validar_cnpj(cnpj_amazon)}")
    print(f"Formatado: {formatar_cnpj(cnpj_amazon)}")
