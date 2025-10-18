import boto3

def get_last_folder_in_production(bucket_name, prefix='produccion/'):
    """
    Retorna el nombre de la última subcarpeta dentro de produccion/
    
    Args:
        bucket_name: Nombre del bucket S3
        prefix: Prefijo de la carpeta base (default: 'produccion/')
    
    Returns:
        str: Nombre de la última carpeta (ej: '2025-09/')
        None: Si no se encuentra ninguna carpeta
    """
    s3 = boto3.client('s3')
    
    # Listar todos los objetos dentro de produccion/
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    
    if 'Contents' not in response:
        print(f"No hay contenido en {prefix}")
        return None
    
    # Extraer subcarpetas dentro de produccion/
    subfolders = {}
    for obj in response['Contents']:
        key = obj['Key']
        
        # Remover el prefijo 'produccion/' y verificar si hay más niveles
        relative_path = key[len(prefix):]
        
        if '/' in relative_path:
            # Extraer la primera subcarpeta después de produccion/
            subfolder_name = relative_path.split('/')[0]
            full_subfolder = prefix + subfolder_name + '/'
            
            if full_subfolder not in subfolders:
                subfolders[full_subfolder] = obj['LastModified']
            else:
                # Actualizar si encontramos un archivo más reciente
                if obj['LastModified'] > subfolders[full_subfolder]:
                    subfolders[full_subfolder] = obj['LastModified']
    
    if not subfolders:
        print(f"No se encontraron subcarpetas en {prefix}")
        return None
    
    # Encontrar la subcarpeta más reciente
    last_subfolder = max(subfolders.items(), key=lambda x: x[1])
    last_subfolder_name = last_subfolder[0]
    
    # Extraer solo el nombre de la carpeta sin 'produccion/'
    folder_name_only = last_subfolder_name.replace(prefix, '')
    
    return folder_name_only


# Uso

BUCKET_NAME = "xideralaws-curso-jonathan"
carpeta = get_last_folder_in_production(BUCKET_NAME)

print(carpeta)