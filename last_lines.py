"""
Script para resolução do exercício 2: Leitura de arquivo em ordem reversa
"""
import os
import io


def last_lines(file_path, chunk_size=io.DEFAULT_BUFFER_SIZE):
    """
    Retorna um iterador que percorre as linhas de um arquivo em ordem reversa.

    O arquivo é lido em blocos (chunks) para evitar carregar tudo na memória.
    A função garante que:
    - Não quebra caracteres UTF-8 no meio
    - Reconstrói corretamente linhas que atravessam blocos

    Args:
        file_path (str): caminho do arquivo
        chunk_size (int): tamanho máximo de leitura por vez

    Yields:
        str: linhas do arquivo em ordem reversa (com '\n')
    """
    with open(file_path, 'rb') as f: 
        f.seek(0, os.SEEK_END)
        position = f.tell() #posicao inicial do final do arquivo
        
        buffer = b"" # armazena linha incompleta entre chunks
        
        while position > 0:
            read_size = min(chunk_size, position) #le no maximo o tamanho do chunk definido
            position -= read_size #anda para trás no tamanho do chunk
            
            f.seek(position) 
            chunk = f.read(read_size)
            
            data = chunk + buffer #completa com buffer do chunk anterior se houver
            parts = data.split(b'\n') #divide por quebra de linha
            
            buffer = parts[0]  # possível linha incompleta
            
            # linhas completas (em ordem reversa)
            for line in reversed(parts[1:]):
                yield line.decode('utf-8').rstrip('\r') + '\n'
        
        # última linha (ou única linha sem \n no arquivo)
        if buffer:
            yield buffer.decode('utf-8').rstrip('\r') + '\n'

#testando para exemplo do exercicio
if __name__ == "__main__":
    lines = last_lines('my_file.txt')
    print(next(lines))
    print(next(lines))
    print(next(lines))