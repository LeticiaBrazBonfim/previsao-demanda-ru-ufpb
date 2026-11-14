# Como contribuir

## Branches

- `main`: versão oficial. Somente a conta proprietária decide e realiza integrações. O mock só entra nessa branch após decisão explícita.
- `develop/mock`: integração do trabalho com dados sintéticos. Mudanças entram por Pull Request (PR), com duas aprovações: uma revisão técnica de outro integrante e a aprovação da conta proprietária. Somente a conta proprietária realiza o merge.
- `feature/<tema>`: trabalho individual. Crie a branch a partir de `develop/mock` e publique nela seus commits.

## Enviar uma mudança

1. Atualize as referências: `git fetch origin`.
2. Crie a branch: `git switch -c feature/<tema> origin/develop/mock`.
3. Faça commits com mensagens que descrevam a mudança.
4. Publique: `git push -u origin feature/<tema>`.
5. Abra um PR de `feature/<tema>` para `develop/mock`. Descreva o que mudou e como conferiu o resultado. Solicite uma revisão técnica de outro integrante e a revisão da conta proprietária.
6. Quem revisa aponta correções no PR; quem abriu o PR aplica as correções e publica novos commits. Após qualquer novo commit, solicite novamente as duas aprovações. Resolva as conversas antes da integração.

Quem abriu o PR não pode aprová-lo. A aprovação técnica deve vir de outro integrante. Aprovações entre integrantes não substituem a aprovação da conta proprietária.

## Atualizar e resolver conflitos

Na sua `feature/*`, execute `git fetch origin` e `git merge origin/develop/mock`. Se houver conflito, edite os arquivos indicados, confira o resultado, execute `git add <arquivos>`, `git commit` e `git push`. Peça nova revisão depois da atualização.

Não faça push, force push, merge, exclusão ou renomeação de `main` ou `develop/mock`. Não publique credenciais, dados reais sensíveis nem o conteúdo local de `docs_agente/`.
