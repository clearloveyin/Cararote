import os
import shutil
import zipfile


def zip_file(in_dir_list, out_dir, zip_name='zipfile'):
    try:
        import zlib
        compression = zipfile.ZIPZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED
    path = os.path.join(out_dir, zip_name)
    if os.path.exists(path):
        os.remove(path)

    z = zipfile.ZipFile(zip_name, mode="w", compression=compression)
    try:
        for in_dir in in_dir_list:
            start = len(in_dir)
            for dirpath, dirs, files in os.walk(in_dir):
                for file in files:
                    z_path = os.path.join(dirpath, file)
                    z.write(z_path, z_path[start:])
        z.close()
        shutil.move(zip_name, out_dir)
        return path
    except Exception as e:
        print(e)
        if z:
            z.close()
    return None