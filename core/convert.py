import subprocess
import os

def convert_audio(input_path, output_format):
    """
    Convierte un archivo de audio usando FFmpeg
    
    Args:
        input_path (str): Ruta del archivo de entrada
        output_format (str): Formato de salida (ej: 'mp3', 'wav')
    
    Returns:
        str: Ruta del archivo convertido
    
    Raises:
        FileNotFoundError: Si el archivo no existe
        RuntimeError: Si falla la conversión
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"El archivo {input_path} no existe")
    
    filename = os.path.basename(input_path)
    base, _ = os.path.splitext(filename)
    output_filename = f"{base}_convertido.{output_format}"
    output_path = os.path.join(os.path.dirname(input_path), output_filename)
    
    try:
        result = subprocess.run(
            ['ffmpeg', '-i', input_path, '-y', output_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            error_msg = result.stderr if result.stderr else "Error desconocido en FFmpeg"
            raise RuntimeError(f"FFmpeg error: {error_msg}")
        
        return output_path
    
    except Exception as e:
        raise RuntimeError(f"Error en la conversión: {str(e)}")