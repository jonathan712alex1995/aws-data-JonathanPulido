import boto3

def get_last_file_in_folder(bucket_name, folder_path):
    """
    Retorna el nombre del último archivo dentro de una carpeta específica
    
    Args:
        bucket_name: Nombre del bucket S3
        folder_path: Ruta de la carpeta (ej: 'produccion/2025-09/')
    
    Returns:
        str: Nombre del último archivo (ej: 'produccion_2025-09-08.csv')
        None: Si no se encuentra ningún archivo
    """
    s3 = boto3.client('s3')
    
    # Listar todos los objetos dentro de la carpeta
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_path)
    
    if 'Contents' not in response:
        print(f"No hay contenido en {folder_path}")
        return None
    
    # Obtener archivos de la carpeta (excluir la carpeta misma)
    files_in_folder = [
        obj for obj in response['Contents'] 
        if obj['Key'] != folder_path
        and not obj['Key'].endswith('/')  # Excluir subcarpetas
    ]
    
    if not files_in_folder:
        print("No hay archivos en la carpeta")
        return None
    
    # Obtener el archivo más reciente
    last_file = max(files_in_folder, key=lambda x: x['LastModified'])
    
    # Extraer solo el nombre del archivo
    file_name_only = last_file['Key'].split('/')[-1]
    
    return file_name_only


# Uso
if __name__ == "__main__":
    BUCKET_NAME = "xideralaws-curso-jonathan"
    carpeta = "produccion/2025-09/"  # Usar el resultado del script anterior
    archivo = get_last_file_in_folder(BUCKET_NAME, carpeta)
    print(archivo)