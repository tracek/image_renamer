#!/usr/bin/env python3

from PIL import Image
from glob import glob
import time
import os
import shutil
import click


@click.command()
@click.option('--path', type=click.Path(exists=True), help='Path to images.', required=True)
@click.option('--output', prompt='Output directory', help='Output dir.')
@click.option('--prefix', help='Optional prefix')
@click.option("--dry", is_flag=True, show_default=True, default=False, help='Dry run')
@click.option('--date_format', default='%Y-%m-%d_')
def process_images(path, output, prefix, dry, date_format):
    """Batch image renamer - from Q with love"""
    image_paths = glob(os.path.join(path, '**/*'), recursive=True)
    if len(image_paths) == 0:
        print('No files found')

    os.makedirs(output, exist_ok=True)
    for image_path in image_paths:
        try:
            if os.path.splitext(image_path)[1].lower() not in ['.jpg', '.png']:
                continue
            img = Image.open(image_path)
            exif_data = img._getexif()
            exif_image_date = exif_data[306]
            image_date = time.strptime(exif_image_date, '%Y:%m:%d %H:%M:%S')
            new_file_name = time.strftime(date_format, image_date) + os.path.basename(image_path)
            if prefix:
                new_file_name = prefix + new_file_name
            new_path = os.path.join(output, new_file_name)
            # new_path = path.dirname(image_path) + os.sep + new_file_name
            if dry:
                print(image_path + ' -> ' + new_path)
            else:
                shutil.copy(image_path, new_path)
        except (TypeError, KeyError) as e:
            print(f'No EXIF date Information found for file: {image_path}')
        except:
            print(f'Failed to process {image_path}')
            raise


if __name__ == '__main__':
    process_images()


