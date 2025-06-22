import subprocess
import os
import shutil

def convert_audio(input_path, output_format, output_dir=None):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")
    
    if shutil.which('ffmpeg') is None:
        raise RuntimeError("FFmpeg is not installed or not found in system PATH")
    
    output_directory = output_dir if output_dir else os.path.dirname(input_path)
    
    os.makedirs(output_directory, exist_ok=True)
    
    filename = os.path.basename(input_path)
    base, ext = os.path.splitext(filename)
    output_filename = f"{base}_converted.{output_format}"
    output_path = os.path.join(output_directory, output_filename)
    
    counter = 1
    while os.path.exists(output_path):
        output_filename = f"{base}_converted_{counter}.{output_format}"
        output_path = os.path.join(output_directory, output_filename)
        counter += 1
    
    try:
        result = subprocess.run(
            ['ffmpeg', '-i', input_path, '-y', output_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else "Unknown FFmpeg error"
            raise RuntimeError(f"FFmpeg error: {error_msg}")
        
        if not os.path.exists(output_path):
            raise RuntimeError("Conversion failed: Output file was not created")
        return output_path
    
    except Exception as e:
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        raise RuntimeError(f"Conversion error: {str(e)}")
    
    