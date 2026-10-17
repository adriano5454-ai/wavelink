"""Corcovado-only localization of reviewed, repository-owned gateway assets.

Call before substituting the company name. Nothing from the disk's user records
or browser input is passed through the fixed template replacements below.
"""
from app.localization import PT_BR
from app.password_policy import password_min_length

GATEWAY_PT_BR = {
    'WAVELINK / COMPANY WORKSPACE': 'WAVELINK / AMBIENTE DA EMPRESA',
    'WAVELINK / COMPANY SETUP': 'WAVELINK / CONFIGURAÇÃO DA EMPRESA',
    'First sign-in pending': 'Primeiro acesso pendente',
    'The administrator must finish the private first sign-in before this workspace opens.': 'O administrador precisa concluir o primeiro acesso privado antes de liberar o ambiente da empresa.',
    'Use the private setup link provided to the installation operator. Ordinary users do not need that link once setup is complete.': 'Use o link privado de configuração fornecido ao administrador da instalação. Os demais usuários não precisam desse link após a conclusão.',
    'Choose your permanent administrator passphrase before opening the company workspace. This one-time setup does not import the demonstration.': 'Defina sua senha permanente de administrador antes de abrir o ambiente da empresa. Esta configuração é feita uma única vez e não importa os dados da demonstração.',
    'User ID': 'Usuário',
    'Temporary password': 'Senha temporária',
    'Repeat new passphrase': 'Repita a nova senha',
    'New passphrase': 'Nova senha',
    '14–128 characters. A few unrelated words make a memorable passphrase.': 'De 14 a 128 caracteres. Algumas palavras sem relação entre si ajudam a criar uma senha fácil de lembrar.',
    'Set passphrase & finish setup': 'Definir senha e concluir configuração',
    'Check saved outcome': 'Consultar resultado salvo',
    'Open normal Wavelink login →': 'Abrir acesso normal ao Wavelink →',
    'First sign-in is complete. Use your new passphrase at the normal Wavelink login.': 'O primeiro acesso foi concluído. Use sua nova senha para entrar normalmente no Wavelink.',
    'First sign-in was refused.': 'O primeiro acesso foi recusado.',
    'Open the private first sign-in link supplied to the operator.': 'Abra o link privado de primeiro acesso fornecido ao administrador.',
    'The new passphrases do not match.': 'As novas senhas não são iguais.',
    'Saving the new administrator passphrase…': 'Salvando a nova senha do administrador…',
    'Outcome not confirmed.': 'Resultado não confirmado.',
    'Retry unchanged setup': 'Repetir a mesma configuração',
    'The outcome is not confirmed. Retry the same request or check its saved outcome. Do not reset the project.': 'O resultado não foi confirmado. Repita a mesma solicitação ou consulte o resultado salvo. Não reinicialize a empresa.',
    'No completed setup was found for this request. Retry the unchanged setup.': 'Nenhuma configuração concluída foi encontrada para esta solicitação. Repita a mesma configuração.',
    'Outcome unavailable. Keep this page open and retry.': 'Resultado indisponível. Mantenha esta página aberta e tente novamente.',
    'Setup status unavailable. Retry when connected; do not reset the company project.': 'Situação da configuração indisponível. Tente novamente quando houver conexão; não reinicialize os dados da empresa.',
    'Setup status unavailable.': 'Situação da configuração indisponível.',
    'Use the private first sign-in link supplied to the installation operator.': 'Use o link privado de primeiro acesso fornecido ao administrador da instalação.',
    ' · first sign-in': ' · primeiro acesso',
    'First sign-in': 'Primeiro acesso',
}


def localized_asset(text: str, locale: str) -> str:
    if locale != PT_BR:
        return text
    if password_min_length() == 8:
        text = text.replace('minlength="14"', 'minlength="8"').replace(
            '14–128 characters. A few unrelated words make a memorable passphrase.',
            'De 8 a 128 caracteres. Use pelo menos seis caracteres diferentes.')
    text = text.replace('lang="en"', 'lang="pt-BR"')
    for source in sorted(GATEWAY_PT_BR, key=len, reverse=True):
        text = text.replace(source, GATEWAY_PT_BR[source])
    return text
