#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publica os dois PDFs na pasta de credenciais do Drive.

O que ele faz, nesta ordem:

  1. regera os dois PDFs (pule com --sem-gerar);
  2. move para _refugo/ tudo que já estava na pasta de destino;
  3. copia os novos com dia e versão no fim do nome.

Por que mover em vez de sobrescrever: a pasta é de drive compartilhado e
outras pessoas podem ter o link de um arquivo. Sobrescrever trocaria o
conteúdo por baixo de quem já tinha o link; mover preserva o que foi
distribuído e deixa claro qual é o atual.

A versão é um contador global, não por dia: dois PDFs gerados no mesmo dia
precisam de nomes diferentes, e a data sozinha não resolve. Ele sai do maior
_vNN já visto na pasta e no refugo, então nunca reaproveita um número — nem
depois de alguém limpar o refugo pela metade.
"""
import os, re, shutil, subprocess, sys
from datetime import date

AQUI    = os.path.dirname(os.path.abspath(__file__))
DESTINO = ('/Users/locacao2/Library/CloudStorage/GoogleDrive-bernardo@wt.ag/'
           'Drives compartilhados/WT.AG/2026/Criação/WTA_Credenciais/PDF')
REFUGO  = os.path.join(DESTINO, '_refugo')
FONTES  = ('WT.AG_Credenciais_v2_PT.pdf', 'WT.AG_Credenciais_v2_EN.pdf')


def proxima_versao():
    """Maior _vNN visto na pasta e no refugo, mais um."""
    maior = 0
    for pasta in (DESTINO, REFUGO):
        if not os.path.isdir(pasta):
            continue
        for nome in os.listdir(pasta):
            m = re.search(r'_v(\d+)\.pdf$', nome)
            if m:
                maior = max(maior, int(m.group(1)))
    return maior + 1


def main():
    if '--sem-gerar' not in sys.argv:
        print('── gerando os PDFs')
        r = subprocess.run([sys.executable, 'gerar-pdf.py'], cwd=AQUI)
        if r.returncode:
            sys.exit('! gerar-pdf.py falhou; nada foi publicado')

    faltam = [f for f in FONTES if not os.path.exists(os.path.join(AQUI, f))]
    if faltam:
        sys.exit('! não encontrei: %s' % ', '.join(faltam))

    if not os.path.isdir(DESTINO):
        sys.exit('! pasta de destino não encontrada — o Drive está montado?\n  %s' % DESTINO)

    os.makedirs(REFUGO, exist_ok=True)

    print('\n── refugo')
    movidos = 0
    for nome in sorted(os.listdir(DESTINO)):
        velho = os.path.join(DESTINO, nome)
        if not os.path.isfile(velho) or not nome.lower().endswith('.pdf'):
            continue
        alvo = os.path.join(REFUGO, nome)
        # não atropela um homônimo que já esteja no refugo
        base, ext = os.path.splitext(nome)
        n = 2
        while os.path.exists(alvo):
            alvo = os.path.join(REFUGO, '%s (%d)%s' % (base, n, ext)); n += 1
        shutil.move(velho, alvo)
        print('   %s → _refugo/%s' % (nome, os.path.basename(alvo)))
        movidos += 1
    if not movidos:
        print('   (a pasta estava vazia)')

    v = proxima_versao()
    hoje = date.today().strftime('%d.%m.%Y')
    print('\n── publicando  ·  %s  ·  v%02d' % (hoje, v))
    for f in FONTES:
        base = f[:-4]                                   # sem .pdf
        novo = '%s_%s_v%02d.pdf' % (base, hoje, v)
        shutil.copy2(os.path.join(AQUI, f), os.path.join(DESTINO, novo))
        mb = os.path.getsize(os.path.join(DESTINO, novo)) / 1e6
        print('   %-52s %5.1f MB' % (novo, mb))

    print('\npronto. %d arquivo(s) para o refugo, 2 publicados.' % movidos)


if __name__ == '__main__':
    main()
