import os
import io


def last_lines(file_path, chunk_size=io.DEFAULT_BUFFER_SIZE):
    with open(file_path, 'rb') as f:
        f.seek(0, os.SEEK_END)
        position = f.tell()
        
        buffer = b""
        
        while position > 0:
            read_size = min(chunk_size, position)
            position -= read_size
            
            f.seek(position)
            chunk = f.read(read_size)
            
            data = chunk + buffer
            parts = data.split(b'\n')
            
            buffer = parts[0]  # possível linha incompleta
            
            # linhas completas (em ordem reversa)
            for line in reversed(parts[1:]):
                yield line.decode('utf-8').rstrip('\r') + '\n'
        
        # última linha (ou única linha sem \n no arquivo)
        if buffer:
            yield buffer.decode('utf-8').rstrip('\r') + '\n'

if __name__ == "__main__":
    lines = last_lines('my_file.txt')
    print(next(lines))
    print(next(lines))
    print(next(lines))