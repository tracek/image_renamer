#!/usr/bin/env python3

from PIL import Image
from glob import glob
from datetime import datetime
import time
import os
import shutil
import click


@click.command()
@click.option('--path', type=click.Path(exists=True), help='Path to images.', required=True)
@click.option('--output', prompt='Output directory', help='Output dir.')
@click.option('--prefix', help='Optional prefix')
@click.option("--dry", is_flag=True, show_default=True, default=False, help='Dry run')
@click.option('--date_format', default='%Y-%m-%d')
def process_images(path, output, prefix, dry, date_format):
    """Batch image renamer - from Q with love"""
    image_paths = glob(os.path.join(path, '**/*'), recursive=True)
    if len(image_paths) == 0:
        print('No files found')

    os.makedirs(output, exist_ok=True)
    for idx, image_path in enumerate(image_paths):
        try:
            extension = os.path.splitext(image_path)[1]
            if extension.lower() not in ['.jpg', '.png']:
                continue
            img = Image.open(image_path)
            exif_data = img._getexif()
            try:
                exif_image_date = exif_data[306]
                image_date = time.strptime(exif_image_date, '%Y:%m:%d %H:%M:%S')
                image_date = time.strftime(date_format, image_date)
            except:
                print(f'No EXIF date Information found for file: {image_path}. '
                      f'Using file creation / modification time instead')
                image_date = datetime.utcfromtimestamp(int(os.path.getctime(image_path))).strftime('%Y-%m-%d')

            new_file_name = f'{image_date}_{idx:03d}{extension}'

            if prefix:
                new_file_name = prefix + new_file_name
            new_path = os.path.join(output, new_file_name)
            # new_path = path.dirname(image_path) + os.sep + new_file_name
            if dry:
                print(image_path + ' -> ' + new_path)
            else:
                shutil.copy(image_path, new_path)
        except:
            print(f'Failed to process {image_path}')
            raise


if __name__ == '__main__':
    process_images()


