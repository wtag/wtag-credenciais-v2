# Como publicar o Credenciais v2

**Ainda não está publicado.** Esta versão nasceu em 29.09 como cópia da versão
de concorrência e vive só no disco, com histórico de commits mas **sem remote**.

O remote foi removido de propósito: com o histórico herdado, um `git push`
distraído mandaria commits do v2 para o repositório da concorrência.

## Quando for publicar

1. Criar o repositório **vazio** na organização (sem README, sem `.gitignore`,
   sem licença — qualquer arquivo criado pelo GitHub faz o primeiro push ser
   recusado).
2. Apontar o remote e empurrar:

   ```bash
   cd ~/Projetos/wtag-credenciais-v2
   git remote add origin https://github.com/wtag/<nome-do-repo>.git
   git push -u origin main
   ```

3. Preencher `DECK_ONLINE` no `gerar-pdf.py` com a URL do Pages. Enquanto ela
   estiver vazia, os vídeos sem arquivo no Drive saem **sem link** — de
   propósito, porque link que leva ao deck de outra versão é pior que link
   nenhum.
4. **Settings → Pages** · Source `Deploy from a branch` · Branch `main` ·
   pasta `/ (root)`.

A autenticação está no **GitHub Desktop**, não no chaveiro do git de linha de
comando.

## O que NÃO pode entrar no repositório

O mesmo de sempre, e vale desde o primeiro commit:

- **`Claude outputs/`** — pasta onde o app deixa os arquivos anexados. O
  briefing da concorrência **não foi copiado para cá**, justamente por ser
  sensível; se algum anexo novo cair aí, ele não sobe.
- **`WT.AG_*.pdf`** — binário que muda inteiro a cada geração.
- **`assets/img/capascases/`** — fotos de origem das capas. Master não entra no
  repositório, mesma regra dos vídeos em alta.
